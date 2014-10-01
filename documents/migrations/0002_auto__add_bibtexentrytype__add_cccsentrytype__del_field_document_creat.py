# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BibTexEntryType'
        db.create_table(u'documents_bibtexentrytype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=512)),
            ('plural_name', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
        ))
        db.send_create_signal(u'documents', ['BibTexEntryType'])

        # Adding model 'CCCSEntryType'
        db.create_table(u'documents_cccsentrytype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=512)),
            ('plural_name', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
        ))
        db.send_create_signal(u'documents', ['CCCSEntryType'])

        # Deleting field 'Document.creator'
        db.delete_column(u'documents_document', 'creator')

        # Adding field 'Document.author'
        db.add_column(u'documents_document', 'author',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.editor'
        db.add_column(u'documents_document', 'editor',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.year'
        db.add_column(u'documents_document', 'year',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.chapter'
        db.add_column(u'documents_document', 'chapter',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.journal'
        db.add_column(u'documents_document', 'journal',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.volume'
        db.add_column(u'documents_document', 'volume',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.issue'
        db.add_column(u'documents_document', 'issue',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.pages'
        db.add_column(u'documents_document', 'pages',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.series'
        db.add_column(u'documents_document', 'series',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.language'
        db.add_column(u'documents_document', 'language',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.publisher'
        db.add_column(u'documents_document', 'publisher',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.institution'
        db.add_column(u'documents_document', 'institution',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.address'
        db.add_column(u'documents_document', 'address',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.cccs_source_path'
        db.add_column(u'documents_document', 'cccs_source_path',
                      self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.bibtex_entry_type'
        db.add_column(u'documents_document', 'bibtex_entry_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.BibTexEntryType'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.cccs_entry_type'
        db.add_column(u'documents_document', 'cccs_entry_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.CCCSEntryType'], null=True, blank=True),
                      keep_default=False)

        # Adding M2M table for field countries on 'Document'
        m2m_table_name = db.shorten_name(u'documents_document_countries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('document', models.ForeignKey(orm[u'documents.document'], null=False)),
            ('country', models.ForeignKey(orm[u'projects.country'], null=False))
        ))
        db.create_unique(m2m_table_name, ['document_id', 'country_id'])


    def backwards(self, orm):
        # Deleting model 'BibTexEntryType'
        db.delete_table(u'documents_bibtexentrytype')

        # Deleting model 'CCCSEntryType'
        db.delete_table(u'documents_cccsentrytype')

        # Adding field 'Document.creator'
        db.add_column(u'documents_document', 'creator',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Document.author'
        db.delete_column(u'documents_document', 'author')

        # Deleting field 'Document.editor'
        db.delete_column(u'documents_document', 'editor')

        # Deleting field 'Document.year'
        db.delete_column(u'documents_document', 'year')

        # Deleting field 'Document.chapter'
        db.delete_column(u'documents_document', 'chapter')

        # Deleting field 'Document.journal'
        db.delete_column(u'documents_document', 'journal')

        # Deleting field 'Document.volume'
        db.delete_column(u'documents_document', 'volume')

        # Deleting field 'Document.issue'
        db.delete_column(u'documents_document', 'issue')

        # Deleting field 'Document.pages'
        db.delete_column(u'documents_document', 'pages')

        # Deleting field 'Document.series'
        db.delete_column(u'documents_document', 'series')

        # Deleting field 'Document.language'
        db.delete_column(u'documents_document', 'language')

        # Deleting field 'Document.publisher'
        db.delete_column(u'documents_document', 'publisher')

        # Deleting field 'Document.institution'
        db.delete_column(u'documents_document', 'institution')

        # Deleting field 'Document.address'
        db.delete_column(u'documents_document', 'address')

        # Deleting field 'Document.cccs_source_path'
        db.delete_column(u'documents_document', 'cccs_source_path')

        # Deleting field 'Document.bibtex_entry_type'
        db.delete_column(u'documents_document', 'bibtex_entry_type_id')

        # Deleting field 'Document.cccs_entry_type'
        db.delete_column(u'documents_document', 'cccs_entry_type_id')

        # Removing M2M table for field countries on 'Document'
        db.delete_table(db.shorten_name(u'documents_document_countries'))


    models = {
        u'documents.bibtexentrytype': {
            'Meta': {'ordering': "['name']", 'object_name': 'BibTexEntryType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512'}),
            'plural_name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        u'documents.cccsentrytype': {
            'Meta': {'ordering': "['name']", 'object_name': 'CCCSEntryType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512'}),
            'plural_name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        u'documents.document': {
            'Meta': {'object_name': 'Document'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'bibtex_entry_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['documents.BibTexEntryType']", 'null': 'True', 'blank': 'True'}),
            'cccs_entry_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['documents.CCCSEntryType']", 'null': 'True', 'blank': 'True'}),
            'cccs_source_path': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'chapter': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'documents'", 'symmetrical': 'False', 'to': u"orm['projects.Country']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'editor': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'issue': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'journal': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            u'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'pages': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'series': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'source_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'volume': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'projects.country': {
            'Meta': {'object_name': 'Country'},
            'fips': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso': ('django.db.models.fields.CharField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'iso_3166': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'iso_english_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'iso_numeric': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'plural_name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['documents']