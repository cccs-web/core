from django.contrib import admin

from categories.admin import CategoryBaseAdmin

import documents.models as dm


class DocumentCategoryAdmin(CategoryBaseAdmin):
    pass

admin.site.register(dm.DocumentCategory, DocumentCategoryAdmin)


class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'updated']
    list_filter = ['tags']
    fieldsets = ((None, {'fields': ('title',
                                    'source_file',
                                    'original_source_filename',
                                    'author',
                                    'editor',
                                    'tags',
                                    'content',
                                    'year',
                                    'chapter',
                                    'journal',
                                    'volume',
                                    'issue',
                                    'pages',
                                    'series',
                                    'language',
                                    'publisher',
                                    'institution',
                                    'address',
                                    'categories')}),
                 ('Metadata', {'classes': ('collapse-closed',),
                               'fields': ('_meta_title',
                                          'slug',
                                          'short_url',
                                          'description',
                                          'gen_description',
                                          'keywords',
                                          'publish_date',
                                          'expiry_date')}))
    filter_horizontal = ('categories',)

    def save_model(self, request, obj, form, change):
        obj.original_source_filename = request.FILES['source_file'].name
        super(DocumentAdmin, self).save_model(request, obj, form, change)


admin.site.register(dm.Document, DocumentAdmin)
admin.site.register(dm.BibTexEntryType, admin.ModelAdmin)
admin.site.register(dm.CCCSEntryType, admin.ModelAdmin)