"""
Load in initial data using the source excel spreadsheets
"""
from openpyxl import load_workbook

import cvs.models as cm
from cvs.importers.globals import *


def load_all():
    load_countries('.country-calc, CCCS')
    load_themes('.theme-calc, CCCS', cm.CCCSTheme, cm.CCCSSubTheme)
    load_themes('.theme-calc, IFC', cm.IFCTheme, cm.IFCSubTheme)
    load_ifc_sectors('.sector-calc, IFC')
    load_cccs_sectors('.sector-calc, CCCS', cm.CCCSSector, cm.CCCSSubSector)
    load_projects('PROJECT')


def load_countries(sheet_name):
    country_dicts = get_country_dicts(sheet_name)
    for info in country_dicts:
        country, _ = cm.Country.objects.get_or_create(name=info['name'])
        for (k, v) in info.iteritems():
            setattr(country, k, v)
        country.save()


def get_country_dicts(sheet_name):
    """
    Use the gold cv to obtain the list of countries and related data
    Go for the '.country-calc, CCCS' sheet and collect the data from row 4 to the end.
    """
    wb = load_workbook(filename=xlsx_cv)
    ws = wb.get_sheet_by_name(sheet_name)

    countries = list()
    for row in ws.rows[3:]:  # ignore first three rows
        if row[0].value is None:
            continue  # ignore null entries
        countries.append({
            'name': row[0].value,
            'iso_english_name': row[1].value,
            'fips': row[2].value,
            'iso_numeric': row[3].value,
            'iso_3166': row[4].value,
            'iso': row[5].value,
            'notes': row[6].value})
    return countries


def load_themes(sheet_name, theme_model, sub_theme_model):
    theme_dict = get_theme_dict(sheet_name)
    for (theme_name, sub_theme_names) in theme_dict.iteritems():
        theme, created = theme_model.objects.get_or_create(name=theme_name)
        if created:
            theme.save()
        for sub_theme_name in sub_theme_names:
            sub_theme, created = sub_theme_model.objects.get_or_create(theme=theme, name=sub_theme_name)
            if created:
                sub_theme.save()


def get_theme_dict(sheet_name):
    """
    Use the gold cv to obtain all the cccs themes and sub themes
    """
    wb = load_workbook(filename=xlsx_cv)
    ws = wb.get_sheet_by_name(sheet_name)

    themes = dict()
    for row in ws.rows[1:]:  # ignore heading row
        theme_name = row[3].value
        sub_theme_name = row[4].value
        if theme_name is None:
            continue
        if theme_name not in themes:
            themes[theme_name] = set()
        themes[theme_name].add(sub_theme_name)
    return themes


def load_ifc_sectors(sheet_name):
    sector_names = get_ifc_sector_names(sheet_name)
    for sector_name in sector_names:
        sector, created = cm.IFCSector.objects.get_or_create(name=sector_name)
        if created:
            sector.save()


def get_ifc_sector_names(sheet_name):
    """
    Use the gold cv to obtain all the IFC sectors
    """
    wb = load_workbook(filename=xlsx_cv)
    ws = wb.get_sheet_by_name(sheet_name)
    sector_names = list()
    for row in ws.rows[2:]:  # ignore first two rows
        sector_name = row[1].value
        if sector_name is None:
            continue
        sector_names.append(sector_name)
    return sector_names


def load_cccs_sectors(sheet_name, sector_model, sub_sector_model):
    sector_dict = get_cccs_sector_dict(sheet_name)
    for (sector_name, sub_sector_names) in sector_dict.iteritems():
        sector, created = sector_model.objects.get_or_create(name=sector_name)
        if created:
            sector.save()
        for sub_sector_name in sub_sector_names:
            sub_sector, created = sub_sector_model.objects.get_or_create(sector=sector, name=sub_sector_name)
            if created:
                sub_sector.save()


def get_cccs_sector_dict(sheet_name):
    """
    Use the gold cv to obtain all the cccs themes and sub themes
    """
    wb = load_workbook(filename=xlsx_cv)
    ws = wb.get_sheet_by_name(sheet_name)

    sectors = dict()
    for row in ws.rows[1:]:  # ignore heading row
        sector_name = row[1].value
        sub_sector_name = row[2].value
        if sector_name is None:
            continue
        if sector_name not in sectors:
            sectors[sector_name] = set()
        sectors[sector_name].add(sub_sector_name)
    return sectors


def load_projects(sheet_name):
    projects = get_project_dict(sheet_name)
    for project_name, project_info in projects.iteritems():
        project, _ = cm.Project.objects.get_or_create(name=project_name)
        project.name = project_name
        project.date_range = project_info['Date Range']
        project.loan_or_grant = project_info['Loan/TA/Grant No']
        project.features = project_info['Main Project Features']
        # Multiple countries are allowed but only one from import
        try:
            country = cm.Country.objects.get(name=project_info['Country'])
            project.countries.add(country)
        except cm.Country.DoesNotExist:
            print("No country for \"{0}\": '{1}' does not exist".format(project_name, project_info['Country']))
        # Break Services On/Off-site into flags and have a go at importing them
        services = project_info['Services On/Off-site']
        if services is not None:
            project.service_on_site = 'On' in services
            project.service_off_site = 'Off' in services
            project.service_on_site = 'remote' in services
        project.position = project_info['Position']
        project.client_end = project_info['Sponsor / End Client']
        project.client_contract = project_info['Contracted Through / Direct Client']
        project.client_beneficiary = project_info['Beneficiary Client']
        project.contract = project_info['Contract No.']
        project.person_months = project_info['Person-months']
        project.activities = project_info['Activities Performed']
        project.references = project_info['References']

        cccs_theme_name = project_info['Thematic Issues -GENERAL']
        cccs_subtheme_name = project_info['Sub-Themes -GENERAL']
        try:
            cccs_theme = cm.CCCSTheme.objects.get(name=cccs_theme_name)
            cccs_subtheme = cm.CCCSSubTheme.objects.get(theme=cccs_theme, name=cccs_subtheme_name)
            project.cccs_subtheme = cccs_subtheme
        except (cm.CCCSTheme.DoesNotExist, cm.CCCSSubTheme.DoesNotExist):
            print(u"No cccs_subtheme for {0} ({1}/{2}".format(project_name, cccs_theme_name, cccs_subtheme_name))

        cccs_sector_name = project_info['Sector -GENERAL']
        cccs_subsector_name = project_info['Sub-sector -GENERAL']
        try:
            cccs_sector = cm.CCCSSector.objects.get(name=cccs_sector_name)
            cccs_subsector = cm.CCCSSubSector.objects.get(theme=cccs_sector, name=cccs_subsector_name)
            project.cccs_subsector = cccs_subsector
        except (cm.CCCSSector.DoesNotExist, cm.CCCSSubSector.DoesNotExist):
            print(u"No cccs_subsector for {0} ({1}/{2}".format(project_name, cccs_sector_name, cccs_subsector_name))

        ifc_theme_name = project_info['Thematic Issues -IFC']
        ifc_subtheme_name = project_info['Sub-Themes -IFC']
        try:
            ifc_theme = cm.IFCTheme.objects.get(name=ifc_theme_name)
            ifc_subtheme = cm.IFCSubTheme.objects.get(theme=ifc_theme, name=ifc_subtheme_name)
            project.ifc_subtheme = ifc_subtheme
        except (cm.IFCTheme.DoesNotExist, cm.IFCSubTheme.DoesNotExist):
            print(u"No ifc_subtheme for {0} ({1}/{2})".format(project_name, ifc_theme_name, ifc_subtheme_name))

        ifc_sector_name = project_info['Sector -IFC']
        try:
            ifc_sector = cm.IFCSector.objects.get(name=ifc_sector_name)
            project.ifc_sector = ifc_sector
        except cm.IFCSector.DoesNotExist:
            print(u"No ifc_sector for {0} ({1})".format(project_name, ifc_sector_name))

        project.save()


def get_project_dict(sheet_name):
    projects = dict()
    for cv in xlsx_cvs:
        wb = load_workbook(filename=cv)
        ws = wb.get_sheet_by_name(sheet_name)
        headings = _get_project_dict_headings(ws.rows[0])
        for row in ws.rows[1:]:
            project_name = row[1].value
            if project_name is not None:  # project has a name
                projects[project_name] = {k: c.value for (k, c) in zip(headings, row)}
        return projects


def _get_project_dict_headings(heading_row):
    headings = list()
    for heading_cell in heading_row:
        if heading_cell.value is None:
            break
        headings.append(heading_cell.value.strip())
    return headings
