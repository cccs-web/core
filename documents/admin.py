from django.contrib import admin

import documents.models as dm


class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'updated']
    list_filter = ['tags']
    fieldsets = ((None, {'fields': ('title',
                                    'source_file',
                                    'creator',
                                    'tags',
                                    'content')}),
                 ('Metadata', {'classes': ('collapse-closed',),
                               'fields': ('_meta_title',
                                          'slug',
                                          'short_url',
                                          'description',
                                          'gen_description',
                                          'keywords',
                                          'publish_date',
                                          'expiry_date')}))

admin.site.register(dm.Document, DocumentAdmin)
