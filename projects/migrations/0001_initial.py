# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Country'
        db.create_table(u'projects_country', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=512)),
            ('iso_english_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
            ('fips', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('iso_numeric', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('iso_3166', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('iso', self.gf('django.db.models.fields.CharField')(max_length=7, null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(max_length=512, null=True, blank=True)),
        ))
        db.send_create_signal(u'projects', ['Country'])

        # Adding model 'CCCSTheme'
        db.create_table(u'projects_cccstheme', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=512)),
        ))
        db.send_create_signal(u'projects', ['CCCSTheme'])

        # Adding model 'CCCSSubTheme'
        db.create_table(u'projects_cccssubtheme', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('theme', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subtheme_set', to=orm['projects.CCCSTheme'])),
        ))
        db.send_create_signal(u'projects', ['CCCSSubTheme'])

        # Adding unique constraint on 'CCCSSubTheme', fields ['theme', 'name']
        db.create_unique(u'projects_cccssubtheme', ['theme_id', 'name'])

        # Adding model 'CCCSSector'
        db.create_table(u'projects_cccssector', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=512)),
        ))
        db.send_create_signal(u'projects', ['CCCSSector'])

        # Adding model 'CCCSSubSector'
        db.create_table(u'projects_cccssubsector', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('sector', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sub_themes', to=orm['projects.CCCSSector'])),
        ))
        db.send_create_signal(u'projects', ['CCCSSubSector'])

        # Adding unique constraint on 'CCCSSubSector', fields ['sector', 'name']
        db.create_unique(u'projects_cccssubsector', ['sector_id', 'name'])

        # Adding model 'IFCTheme'
        db.create_table(u'projects_ifctheme', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=512)),
        ))
        db.send_create_signal(u'projects', ['IFCTheme'])

        # Adding model 'IFCSubTheme'
        db.create_table(u'projects_ifcsubtheme', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('theme', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sub_themes', to=orm['projects.IFCTheme'])),
        ))
        db.send_create_signal(u'projects', ['IFCSubTheme'])

        # Adding unique constraint on 'IFCSubTheme', fields ['theme', 'name']
        db.create_unique(u'projects_ifcsubtheme', ['theme_id', 'name'])

        # Adding model 'IFCSector'
        db.create_table(u'projects_ifcsector', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=512)),
        ))
        db.send_create_signal(u'projects', ['IFCSector'])

        # Adding model 'Project'
        db.create_table(u'projects_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'keywords_string', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('title_fr', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('title_ru', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
            ('_meta_title', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('gen_description', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('expiry_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('short_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('in_sitemap', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_range', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('from_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('to_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('loan_or_grant', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('features', self.gf('django.db.models.fields.TextField')(max_length=2048, null=True, blank=True)),
            ('features_en', self.gf('django.db.models.fields.TextField')(max_length=2048, null=True, blank=True)),
            ('features_fr', self.gf('django.db.models.fields.TextField')(max_length=2048, null=True, blank=True)),
            ('features_ru', self.gf('django.db.models.fields.TextField')(max_length=2048, null=True, blank=True)),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('region_en', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('region_fr', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('region_ru', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('locality', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('locality_en', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('locality_fr', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('locality_ru', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('service_on_site', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('service_off_site', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('service_remote', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('client_end', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('client_contract', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('client_beneficiary', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('contract', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
        ))
        db.send_create_signal(u'projects', ['Project'])

        # Adding M2M table for field countries on 'Project'
        m2m_table_name = db.shorten_name(u'projects_project_countries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'projects.project'], null=False)),
            ('country', models.ForeignKey(orm[u'projects.country'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'country_id'])

        # Adding M2M table for field cccs_subthemes on 'Project'
        m2m_table_name = db.shorten_name(u'projects_project_cccs_subthemes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'projects.project'], null=False)),
            ('cccssubtheme', models.ForeignKey(orm[u'projects.cccssubtheme'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'cccssubtheme_id'])

        # Adding M2M table for field cccs_subsectors on 'Project'
        m2m_table_name = db.shorten_name(u'projects_project_cccs_subsectors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'projects.project'], null=False)),
            ('cccssubsector', models.ForeignKey(orm[u'projects.cccssubsector'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'cccssubsector_id'])

        # Adding M2M table for field ifc_subthemes on 'Project'
        m2m_table_name = db.shorten_name(u'projects_project_ifc_subthemes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'projects.project'], null=False)),
            ('ifcsubtheme', models.ForeignKey(orm[u'projects.ifcsubtheme'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'ifcsubtheme_id'])

        # Adding M2M table for field ifc_sectors on 'Project'
        m2m_table_name = db.shorten_name(u'projects_project_ifc_sectors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'projects.project'], null=False)),
            ('ifcsector', models.ForeignKey(orm[u'projects.ifcsector'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'ifcsector_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'IFCSubTheme', fields ['theme', 'name']
        db.delete_unique(u'projects_ifcsubtheme', ['theme_id', 'name'])

        # Removing unique constraint on 'CCCSSubSector', fields ['sector', 'name']
        db.delete_unique(u'projects_cccssubsector', ['sector_id', 'name'])

        # Removing unique constraint on 'CCCSSubTheme', fields ['theme', 'name']
        db.delete_unique(u'projects_cccssubtheme', ['theme_id', 'name'])

        # Deleting model 'Country'
        db.delete_table(u'projects_country')

        # Deleting model 'CCCSTheme'
        db.delete_table(u'projects_cccstheme')

        # Deleting model 'CCCSSubTheme'
        db.delete_table(u'projects_cccssubtheme')

        # Deleting model 'CCCSSector'
        db.delete_table(u'projects_cccssector')

        # Deleting model 'CCCSSubSector'
        db.delete_table(u'projects_cccssubsector')

        # Deleting model 'IFCTheme'
        db.delete_table(u'projects_ifctheme')

        # Deleting model 'IFCSubTheme'
        db.delete_table(u'projects_ifcsubtheme')

        # Deleting model 'IFCSector'
        db.delete_table(u'projects_ifcsector')

        # Deleting model 'Project'
        db.delete_table(u'projects_project')

        # Removing M2M table for field countries on 'Project'
        db.delete_table(db.shorten_name(u'projects_project_countries'))

        # Removing M2M table for field cccs_subthemes on 'Project'
        db.delete_table(db.shorten_name(u'projects_project_cccs_subthemes'))

        # Removing M2M table for field cccs_subsectors on 'Project'
        db.delete_table(db.shorten_name(u'projects_project_cccs_subsectors'))

        # Removing M2M table for field ifc_subthemes on 'Project'
        db.delete_table(db.shorten_name(u'projects_project_ifc_subthemes'))

        # Removing M2M table for field ifc_sectors on 'Project'
        db.delete_table(db.shorten_name(u'projects_project_ifc_sectors'))


    models = {
        u'projects.cccssector': {
            'Meta': {'ordering': "['name']", 'object_name': 'CCCSSector'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512'})
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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512'})
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
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        u'projects.ifcsector': {
            'Meta': {'ordering': "['name']", 'object_name': 'IFCSector'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512'})
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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512'})
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