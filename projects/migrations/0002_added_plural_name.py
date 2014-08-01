# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CCCSSector.plural_name'
        db.add_column(u'projects_cccssector', 'plural_name',
                      self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True),
                      keep_default=False)

        # Adding field 'IFCTheme.plural_name'
        db.add_column(u'projects_ifctheme', 'plural_name',
                      self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Country.plural_name'
        db.add_column(u'projects_country', 'plural_name',
                      self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True),
                      keep_default=False)

        # Adding field 'IFCSector.plural_name'
        db.add_column(u'projects_ifcsector', 'plural_name',
                      self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True),
                      keep_default=False)

        # Adding field 'CCCSTheme.plural_name'
        db.add_column(u'projects_cccstheme', 'plural_name',
                      self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'CCCSSector.plural_name'
        db.delete_column(u'projects_cccssector', 'plural_name')

        # Deleting field 'IFCTheme.plural_name'
        db.delete_column(u'projects_ifctheme', 'plural_name')

        # Deleting field 'Country.plural_name'
        db.delete_column(u'projects_country', 'plural_name')

        # Deleting field 'IFCSector.plural_name'
        db.delete_column(u'projects_ifcsector', 'plural_name')

        # Deleting field 'CCCSTheme.plural_name'
        db.delete_column(u'projects_cccstheme', 'plural_name')


    models = {
        u'projects.cccssector': {
            'Meta': {'ordering': "['name']", 'object_name': 'CCCSSector'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512'}),
            'plural_name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        u'projects.cccssubsector': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('sector', 'name'),)", 'object_name': 'CCCSSubSector'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sub_themes'", 'to': u"orm['projects.CCCSSector']"})
        },
        u'projects.cccssubtheme': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('theme', 'name'),)", 'object_name': 'CCCSSubTheme'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'theme': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subtheme_set'", 'to': u"orm['projects.CCCSTheme']"})
        },
        u'projects.cccstheme': {
            'Meta': {'ordering': "['name']", 'object_name': 'CCCSTheme'},
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
        u'projects.ifcsector': {
            'Meta': {'ordering': "['name']", 'object_name': 'IFCSector'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512'}),
            'plural_name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        u'projects.ifcsubtheme': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('theme', 'name'),)", 'object_name': 'IFCSubTheme'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'theme': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sub_themes'", 'to': u"orm['projects.IFCTheme']"})
        },
        u'projects.ifctheme': {
            'Meta': {'ordering': "['name']", 'object_name': 'IFCTheme'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512'}),
            'plural_name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        u'projects.project': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Project'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'cccs_subsectors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'projects'", 'symmetrical': 'False', 'to': u"orm['projects.CCCSSubSector']"}),
            'cccs_subthemes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'projects'", 'symmetrical': 'False', 'to': u"orm['projects.CCCSSubTheme']"}),
            'client_beneficiary': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'client_contract': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'client_end': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'contract': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'projects'", 'symmetrical': 'False', 'to': u"orm['projects.Country']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_range': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'features': ('django.db.models.fields.TextField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'features_en': ('django.db.models.fields.TextField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'features_fr': ('django.db.models.fields.TextField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'features_ru': ('django.db.models.fields.TextField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'from_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ifc_sectors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'projects'", 'symmetrical': 'False', 'to': u"orm['projects.IFCSector']"}),
            'ifc_subthemes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'projects'", 'symmetrical': 'False', 'to': u"orm['projects.IFCSubTheme']"}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'loan_or_grant': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'locality': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'locality_en': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'locality_fr': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'locality_ru': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'region_en': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'region_fr': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'region_ru': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'service_off_site': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service_on_site': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service_remote': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'title_fr': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'title_ru': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'to_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['projects']