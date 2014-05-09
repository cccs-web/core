from django.contrib import admin

import cvs.models as cm


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso_english_name', 'fips', 'iso_numeric', 'iso_3166', 'iso', 'notes')

admin.site.register(cm.Country, CountryAdmin)


class CCCSSubThemeInline(admin.TabularInline):
    model = cm.CCCSSubTheme
    extra = 1


class CCCSThemeAdmin(admin.ModelAdmin):
    inlines = [
        CCCSSubThemeInline]

admin.site.register(cm.CCCSTheme, CCCSThemeAdmin)


class IFCSubThemeInline(admin.TabularInline):
    model = cm.IFCSubTheme
    extra = 1


class IFCThemeAdmin(admin.ModelAdmin):
    inlines = [
        IFCSubThemeInline]

admin.site.register(cm.IFCTheme, IFCThemeAdmin)


class IFCSectorAdmin(admin.ModelAdmin):
    pass

admin.site.register(cm.IFCSector, IFCSectorAdmin)