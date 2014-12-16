# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Author'
        db.create_table(u'documents_author', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=512)),
            ('plural_name', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
        ))
        db.send_create_signal(u'documents', ['Author'])

        # Adding model 'FileName'
        db.create_table(u'documents_filename', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=512)),
            ('plural_name', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
        ))
        db.send_create_signal(u'documents', ['FileName'])

        # Adding model 'Editor'
        db.create_table(u'documents_editor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=512)),
            ('plural_name', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
        ))
        db.send_create_signal(u'documents', ['Editor'])

        # Adding model 'Url'
        db.create_table(u'documents_url', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=512)),
            ('plural_name', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
        ))
        db.send_create_signal(u'documents', ['Url'])

        # Deleting field 'Document.original_source_filename'
        db.delete_column(u'documents_document', 'original_source_filename')

        # Deleting field 'Document.institution'
        db.delete_column(u'documents_document', 'institution')

        # Deleting field 'Document.publisher'
        db.delete_column(u'documents_document', 'publisher')

        # Deleting field 'Document.address'
        db.delete_column(u'documents_document', 'address')

        # Deleting field 'Document.author'
        db.delete_column(u'documents_document', 'author')

        # Deleting field 'Document.editor'
        db.delete_column(u'documents_document', 'editor')

        # Adding field 'Document.month'
        db.add_column(u'documents_document', 'month',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.day'
        db.add_column(u'documents_document', 'day',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.publishing_agency'
        db.add_column(u'documents_document', 'publishing_agency',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.publishing_house'
        db.add_column(u'documents_document', 'publishing_house',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.publisher_city'
        db.add_column(u'documents_document', 'publisher_city',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.publisher_address'
        db.add_column(u'documents_document', 'publisher_address',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.date_received'
        db.add_column(u'documents_document', 'date_received',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.receiving_team_member'
        db.add_column(u'documents_document', 'receiving_team_member',
                      self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.regions'
        db.add_column(u'documents_document', 'regions',
                      self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.document_id'
        db.add_column(u'documents_document', 'document_id',
                      self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.annotation'
        db.add_column(u'documents_document', 'annotation',
                      self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.notes'
        db.add_column(u'documents_document', 'notes',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding M2M table for field authors on 'Document'
        m2m_table_name = db.shorten_name(u'documents_document_authors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('document', models.ForeignKey(orm[u'documents.document'], null=False)),
            ('author', models.ForeignKey(orm[u'documents.author'], null=False))
        ))
        db.create_unique(m2m_table_name, ['document_id', 'author_id'])

        # Adding M2M table for field editors on 'Document'
        m2m_table_name = db.shorten_name(u'documents_document_editors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('document', models.ForeignKey(orm[u'documents.document'], null=False)),
            ('editor', models.ForeignKey(orm[u'documents.editor'], null=False))
        ))
        db.create_unique(m2m_table_name, ['document_id', 'editor_id'])

        # Adding M2M table for field url on 'Document'
        m2m_table_name = db.shorten_name(u'documents_document_url')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('document', models.ForeignKey(orm[u'documents.document'], null=False)),
            ('url', models.ForeignKey(orm[u'documents.url'], null=False))
        ))
        db.create_unique(m2m_table_name, ['document_id', 'url_id'])

        # Adding M2M table for field filenames on 'Document'
        m2m_table_name = db.shorten_name(u'documents_document_filenames')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('document', models.ForeignKey(orm[u'documents.document'], null=False)),
            ('filename', models.ForeignKey(orm[u'documents.filename'], null=False))
        ))
        db.create_unique(m2m_table_name, ['document_id', 'filename_id'])


    def backwards(self, orm):
        # Deleting model 'Author'
        db.delete_table(u'documents_author')

        # Deleting model 'FileName'
        db.delete_table(u'documents_filename')

        # Deleting model 'Editor'
        db.delete_table(u'documents_editor')

        # Deleting model 'Url'
        db.delete_table(u'documents_url')

        # Adding field 'Document.original_source_filename'
        db.add_column(u'documents_document', 'original_source_filename',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.institution'
        db.add_column(u'documents_document', 'institution',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.publisher'
        db.add_column(u'documents_document', 'publisher',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.address'
        db.add_column(u'documents_document', 'address',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.author'
        db.add_column(u'documents_document', 'author',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.editor'
        db.add_column(u'documents_document', 'editor',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Document.month'
        db.delete_column(u'documents_document', 'month')

        # Deleting field 'Document.day'
        db.delete_column(u'documents_document', 'day')

        # Deleting field 'Document.publishing_agency'
        db.delete_column(u'documents_document', 'publishing_agency')

        # Deleting field 'Document.publishing_house'
        db.delete_column(u'documents_document', 'publishing_house')

        # Deleting field 'Document.publisher_city'
        db.delete_column(u'documents_document', 'publisher_city')

        # Deleting field 'Document.publisher_address'
        db.delete_column(u'documents_document', 'publisher_address')

        # Deleting field 'Document.date_received'
        db.delete_column(u'documents_document', 'date_received')

        # Deleting field 'Document.receiving_team_member'
        db.delete_column(u'documents_document', 'receiving_team_member')

        # Deleting field 'Document.regions'
        db.delete_column(u'documents_document', 'regions')

        # Deleting field 'Document.document_id'
        db.delete_column(u'documents_document', 'document_id')

        # Deleting field 'Document.annotation'
        db.delete_column(u'documents_document', 'annotation')

        # Deleting field 'Document.notes'
        db.delete_column(u'documents_document', 'notes')

        # Removing M2M table for field authors on 'Document'
        db.delete_table(db.shorten_name(u'documents_document_authors'))

        # Removing M2M table for field editors on 'Document'
        db.delete_table(db.shorten_name(u'documents_document_editors'))

        # Removing M2M table for field url on 'Document'
        db.delete_table(db.shorten_name(u'documents_document_url'))

        # Removing M2M table for field filenames on 'Document'
        db.delete_table(db.shorten_name(u'documents_document_filenames'))


    models = {
        u'documents.author': {
            'Meta': {'object_name': 'Author'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512'}),
            'plural_name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        u'documents.bibtexentrytype': {
            'Meta': {'object_name': 'BibTexEntryType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512'}),
            'plural_name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        u'documents.cccsentrytype': {
            'Meta': {'object_name': 'CCCSEntryType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512'}),
            'plural_name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        u'documents.document': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Document'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'annotation': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'documents'", 'symmetrical': 'False', 'to': u"orm['documents.Author']"}),
            'bibtex_entry_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['documents.BibTexEntryType']", 'null': 'True', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'documents'", 'symmetrical': 'False', 'to': u"orm['documents.DocumentCategory']"}),
            'cccs_entry_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['documents.CCCSEntryType']", 'null': 'True', 'blank': 'True'}),
            'cccs_source_path': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'chapter': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'documents'", 'symmetrical': 'False', 'to': u"orm['projects.Country']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_received': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'day': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'document_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'editors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'documents'", 'symmetrical': 'False', 'to': u"orm['documents.Editor']"}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'filenames': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'documents'", 'symmetrical': 'False', 'to': u"orm['documents.FileName']"}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'issue': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'journal': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            u'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'month': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pages': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publisher_address': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'publisher_city': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'publishing_agency': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'publishing_house': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'receiving_team_member': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'regions': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'series': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'sha': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'source_file': ('django.db.models.fields.files.FileField', [], {'max_length': '512'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'url': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'documents'", 'symmetrical': 'False', 'to': u"orm['documents.Url']"}),
            'volume': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'documents.documentcategory': {
            'Meta': {'ordering': "('tree_id', 'lft')", 'unique_together': "(('parent', 'name'),)", 'object_name': 'DocumentCategory'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['documents.DocumentCategory']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '512'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'documents.editor': {
            'Meta': {'object_name': 'Editor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512'}),
            'plural_name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        u'documents.filename': {
            'Meta': {'ordering': "['name']", 'object_name': 'FileName'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512'}),
            'plural_name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        u'documents.url': {
            'Meta': {'object_name': 'Url'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512'}),
            'plural_name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
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