# -*- coding: utf-8 -*-
"""
Remove all unused translatable fields in all models and sync database structure.

You will need to execute this command in two cases:

    1. When you remove languages from settings.LANGUAGES.

"""

from optparse import make_option
from django.conf import settings
from django.core.management.base import NoArgsCommand
from django.db import connection
from django.utils.six import moves

from django.conf.global_settings import LANGUAGES as AVAILABLE_LANGUAGES

from modeltranslation.translator import translator
from modeltranslation.utils import build_localized_fieldname


def ask_for_confirmation(sql_sentences, model_full_name, interactive):
    print('\nSQL to synchronize "%s" schema:' % model_full_name)
    for sentence in sql_sentences:
        print('   %s' % sentence)
    while True:
        prompt = '\nAre you sure that you want to execute the previous SQL: (y/n) [n]: '
        if interactive:
            answer = moves.input(prompt).strip()
        else:
            answer = 'y'
        if answer == '':
            return False
        elif answer not in ('y', 'n', 'yes', 'no'):
            print('Please answer yes or no')
        elif answer == 'y' or answer == 'yes':
            return True
        else:
            return False


def print_bad_langs(bad_langs, field_name, model_name):
    print('bad languages in "%s" field from "%s" model: %s' % (
        field_name, model_name, ", ".join(bad_langs)))


class Command(NoArgsCommand):
    help = ('Removes columns of removed languages',)

    option_list = NoArgsCommand.option_list + (
        make_option('--noinput', action='store_false', dest='interactive', default=True,
                    help='Do NOT prompt the user for input of any kind.'),
    )

    def __init__(self):
        super(Command, self).__init__()
        self.cursor = connection.cursor()
        self.introspection = connection.introspection

    def handle_noargs(self, **options):
        """
        Command execution.
        """
        self.interactive = options['interactive']

        models = translator.get_registered_models(abstract=False)
        found_bad_fields = False
        for model in models:
            db_table = model._meta.db_table
            model_full_name = '%s.%s' % (model._meta.app_label, model._meta.module_name)
            opts = translator.get_options_for_model(model)
            for field_name in opts.local_fields.keys():
                bad_lang_field_names = self.get_bad_lang_field_names(field_name, db_table)
                if bad_lang_field_names:
                    found_bad_fields = True
                    print_bad_langs(bad_lang_field_names, field_name, model_full_name)
                    sql_sentences = self.get_alter_sql(bad_lang_field_names, model)
                    execute_sql = ask_for_confirmation(
                        sql_sentences, model_full_name, self.interactive)
                    if execute_sql:
                        print('Executing SQL...')
                        for sentence in sql_sentences:
                            self.cursor.execute(sentence)
                        print('Done')
                    else:
                        print('SQL not executed')

        if not found_bad_fields:
            print('No new translatable fields detected')

    def get_table_fields(self, db_table):
        """
        Gets table fields from schema.
        """
        db_table_desc = self.introspection.get_table_description(self.cursor, db_table)
        return [t[0] for t in db_table_desc]

    def get_bad_lang_field_names(self, field_name, db_table):
        """
        Gets only excess fields.
        """
        db_table_fields = self.get_table_fields(db_table)
        good_languages = [lang_code for lang_code, _ in settings.LANGUAGES]
        bad_languages = [lang_code for lang_code, _ in AVAILABLE_LANGUAGES
                         if lang_code not in good_languages]
        bad_field_names = [build_localized_fieldname(field_name, lang_code)
                           for lang_code in bad_languages]

        return [field_name for field_name in bad_field_names
                if field_name in db_table_fields]

    @staticmethod
    def get_alter_sql(bad_lang_field_names, model):
        """
        Returns SQL needed for dropping the bad field names.
        """
        qn = connection.ops.quote_name
        sql_output = []
        table_name = model._meta.db_table
        for field_name in bad_lang_field_names:
            sql_output.append("ALTER TABLE {table_name} DROP COLUMN {column_name};".format(
                table_name=qn(table_name),
                column_name=qn(field_name)))
        return sql_output
