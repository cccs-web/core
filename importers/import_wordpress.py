"""
Pragmatic import of pages wordpress into mezzanine.
"""
from django.contrib.auth.models import User
from mezzanine.pages.models import RichTextPage
from kitchen.text.converters import to_bytes, to_unicode


class WordPressImporter(object):

    def __init__(self, verbosity):
        self.verbosity = verbosity
        self.user = User.objects.get(username="paul")

    def vprint(self, msg, verbosity_level=0):
        """
        print if verbosity_level exceeds verbosity
        """
        if self.verbosity >= verbosity_level:
            print(msg)

    @staticmethod
    def get_or_create(model_class, **kwargs):
        """
        Return existing instance if there is one, otherwise create and return a new one.
        """
        # use code/user_group to get asset
        try:
            return model_class.objects.get(**kwargs)
        except model_class.DoesNotExist:
            return model_class(**kwargs)

    def import_pages(self, pages):
        self.vprint("BEGIN Importing pages", 1)
        for page in pages:
            self.import_page(page, pages)
        self.vprint("END   Importing pages", 1)

    def import_page(self, page, pages):
        title = to_unicode(page['post_title'])
        self.vprint("BEGIN Importing page '{0}'".format(to_bytes(title)), 1)
        mezz_page = self.get_or_create(RichTextPage, title=title)
        mezz_page.created = page['post_modified']
        mezz_page.updated = page['post_modified']
        mezz_page.content = to_unicode(page['post_content'])
        mezz_page.save()

        self.vprint("END   Importing page'{0}'".format(to_bytes(title)), 1)


def dictfetchall(cursor):
    """
    Returns all rows from a cursor as a dict
    """
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()]


def get_cursor(db_name, db_username, db_userpassword):
    """
    Return a cursor to use with the specified database.
    """
    from django.db import ConnectionHandler

    source_databases = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': db_name,
            'USER': db_username,
            'PASSWORD': db_userpassword,
            'HOST': '',
            'PORT': ''}}
    return ConnectionHandler(source_databases)['default'].cursor()


def get_metadata(page_id, db_name, db_username, db_userpassword):
    qry = """
SELECT
    *
FROM
    wp_postmeta
WHERE
    post_id = {0}
""".format(page_id)
    cursor = get_cursor(db_name, db_username, db_userpassword)
    cursor.execute(qry)
    metadata = dictfetchall(cursor)
    return {d['meta_key']: d['meta_value'] for d in metadata}


def get_pages(db_name, db_username, db_userpassword):
    """
    Return a full list of the articles as dict rows for further processing.
    This assumes there are not too many (<5,000).
    """
    qry = """
SELECT
    posts.*
FROM
    wp_posts AS posts
WHERE
    post_type = "page" AND
    post_status = "publish";
"""
    cursor = get_cursor(db_name, db_username, db_userpassword)
    cursor.execute(qry)
    pages = dictfetchall(cursor)

    # Remove any pages with no content
    pages = [page for page in pages if len(page['post_content'].strip()) > 0]

    # Add metadata in case I need it
    for page in pages:
        page['metadata'] = get_metadata(page['ID'], db_name, db_username, db_userpassword)
    return pages


def process_command_line(importer_class):
    """
    Process the command line, passing the csv files and parameters to the importer_class
    """
    import argparse

    parser = argparse.ArgumentParser(description="Import WordPress pages and blog entries.")
    parser.add_argument('db_name', help='name of the local mysql database being used for the import')
    parser.add_argument('db_username', help='username to access the local mysql database')
    parser.add_argument('db_userpassword', help='user password to access the local mysql database')
    parser.add_argument('--verbosity', '--v', type=int, choices=[0, 1, 2, 3], default=1,
                        help='controls the amount of information printed \
                        0: nothing, 1: just table (default), 2: row, 3: field')
    args = parser.parse_args()

    importer = importer_class(args.verbosity)
    importer.import_pages(get_pages(args.db_name, args.db_username, args.db_userpassword))

# if __name__ == "__main__":
#     process_command_line(WordPressImporter)