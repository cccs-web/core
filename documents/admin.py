from django.contrib import admin

from categories.admin import CategoryBaseAdmin

import documents.models as dm


class DocumentCategoryAdmin(CategoryBaseAdmin):
    pass

admin.site.register(dm.DocumentCategory, DocumentCategoryAdmin)


class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'updated']
    list_filter = ['tags']
    readonly_fields = ['sha']
    fieldsets = ((None, {'fields': ('title',
                                    'source_file',
                                    'sha',
                                    'authors',
                                    'editors',
                                    'tags',
                                    'content',
                                    'categories')}),
                 ('BibTex', {'classes': ('collapse-closed',),
                             'fields': ('year',
                                        'chapter',
                                        'journal',
                                        'volume',
                                        'issue',
                                        'pages',
                                        'series',
                                        'language',
                                        'publishing_agency',
                                        'publishing_house',
                                        'publisher_city',
                                        'publisher_address')}),
                 ('Metadata', {'classes': ('collapse-closed',),
                               'fields': ('_meta_title',
                                          'slug',
                                          'short_url',
                                          'description',
                                          'gen_description',
                                          'keywords',
                                          'publish_date',
                                          'expiry_date')}))
    filter_horizontal = ('categories', 'authors', 'editors')

    def save_model(self, request, document, form, change):
        super(DocumentAdmin, self).save_model(request, document, form, change)
        filename, created = dm.FileName.objects.get_or_create(name=request.FILES['source_file'].name)
        if created:
            filename.save()
        document.filenames.add(filename)


admin.site.register(dm.Document, DocumentAdmin)
admin.site.register(dm.BibTexEntryType, admin.ModelAdmin)
admin.site.register(dm.CCCSEntryType, admin.ModelAdmin)