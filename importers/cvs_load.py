"""
Load in initial data using the source excel spreadsheets
"""
import datetime
from openpyxl import load_workbook

from mezzanine.utils.urls import slugify

import projects.models as pm
import cvs.models as cm
from importers.cvs_globals import *


# I thought it would be nice to have all the sheet names here for clarity but it isn't. I'm gradually
# phasing them out for literals because it is (for once) clearer.
def load_all():
    load_countries('.country-calc, CCCS')
    load_categorizations(get_theme_dict('.theme-calc, CCCS'), pm.CCCSTheme, pm.CCCSSubTheme, 'theme')
    load_categorizations(get_theme_dict('.theme-calc, IFC'), pm.IFCTheme, pm.IFCSubTheme, 'theme')
    load_ifc_sectors('.sector-calc, IFC')
    load_categorizations(get_cccs_sector_dict('.sector-calc, CCCS'), pm.CCCSSector, pm.CCCSSubSector, 'sector')
    load_projects()
    load_cvs()


def load_countries(sheet_name):
    country_dicts = get_country_dicts(sheet_name)
    for info in country_dicts:
        country, _ = pm.Country.objects.get_or_create(name=info['name'])
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


def load_categorizations(info, theme_model, sub_theme_model, super_field_name):
    for (theme_name, sub_theme_names) in info.iteritems():
        for sub_theme_name in sub_theme_names:
            _load_categorizations(theme_model, theme_name, sub_theme_model, sub_theme_name, super_field_name)


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
        sector, created = pm.IFCSector.objects.get_or_create(name=sector_name)
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


def load_projects():
    projects = get_project_dict()
    for project_name, project_info in projects.iteritems():
        project, _ = pm.Project.objects.get_or_create(title=project_name)
        project.title = project_name

        for (attname, key) in (('date_range', 'Date Range'),
                               ('loan_or_grant', 'Loan/TA/Grant No'),
                               ('features', 'Main Project Features'),
                               ('region', 'Region'),
                               ('position', 'Position'),
                               ('client_end', 'Sponsor / End Client'),
                               ('client_contract', 'Contracted Through / Direct Client'),
                               ('client_beneficiary', 'Beneficiary Client'),
                               ('contract', 'Contract No.'),
                               ('person_months', 'Person-months'),
                               ('activities', 'Activities Performed'),
                               ('references', 'References')):
            setattr(project, attname, project_info.get(key))

        # Multiple countries are allowed but only one from import
        country = get_country(project_info['Country'])
        if country:
            project.countries.add(country)
        else:
            print(u"No country for \"{0}\": '{1}' does not exist".format(project_name, project_info['Country']))

        # Break Services On/Off-site into flags and have a go at importing them
        services = project_info.get('Services On/Off-site', None)
        if services is not None:
            project.service_on_site = 'On' in services
            project.service_off_site = 'Off' in services
            project.service_on_site = 'remote' in services

        for attname, args in (
                ('cccs_subthemes', (pm.CCCSTheme, project_info['Thematic Issues -GENERAL'],
                                    pm.CCCSSubTheme, project_info['Sub-Themes -GENERAL'],
                                    'theme')),
                ('cccs_subsectors', (pm.CCCSSector, project_info['Sector -GENERAL'],
                                     pm.CCCSSubSector, project_info['Sub-sector -GENERAL'],
                                     'sector')),
                ('ifc_subthemes', (pm.IFCTheme, project_info['Thematic Issues -IFC'],
                                   pm.IFCSubTheme, project_info['Sub-Themes -IFC'],
                                   'theme', False))):
            for categorization in _load_categorizations(*args):
                getattr(project, attname).add(categorization)

        ifc_sector_names = get_names_from_string(project_info['Sector -IFC'])
        for ifc_sector_name in ifc_sector_names:
            ifc_sector, created = pm.IFCSector.objects.get_or_create(name=ifc_sector_name)
            if created:
                ifc_sector.save()
            project.ifc_sectors.add(ifc_sector)

        project.save()


def _load_categorizations(super_class, super_values, sub_class, sub_values, super_field, add_unspecified=True):
    """
    Get or create the categorizations returning sub instances
    """
    if super_values:
        super_names = get_names_from_string(super_values)
    else:
        super_names = []
    if sub_values:
        sub_names = get_names_from_string(sub_values)
    else:
        sub_names = []

    if len(super_names) != len(sub_names):
        print("Mismatched theme/subtheme list lengths in cv - using shortest")
    if add_unspecified and not(super_names and sub_names):
        super_names = sub_names = ['Unspecified']

    sub_objects = list()
    for super_name, sub_name in zip(super_names, sub_names):
        super_obj, created = super_class.objects.get_or_create(name=super_name)
        if created:
            super_obj.save()

        sub_kwargs = {super_field: super_obj, 'name': sub_name}
        sub_obj, created = sub_class.objects.get_or_create(**sub_kwargs)
        if created:
            sub_obj.save()
        sub_objects.append(sub_obj)

    return sub_objects


def get_names_from_string(s):
    if s is None:
        return []
    else:
        return [name.strip() for name in s.split(';') if name]


def get_project_dict():
    projects = dict()
    for cv in xlsx_cvs:
        try:
            wb = load_workbook(filename=cv)
        except TypeError:
            print("Unable to open {0}".format(cv))
            continue
        _get_project_dicts_from_wb(wb, projects)
    return projects


def _get_project_dicts_from_wb(wb, projects=None):
    """
    Get project dicts from ws, adding them into projects if supplied.
    """
    if projects is None:
        projects = dict()
    ws = wb.get_sheet_by_name('PROJECT')
    headings = _get_project_dict_headings(ws.rows[0])
    for row in ws.rows[1:]:
        project_name = row[1].value
        if project_name is not None:
            if project_name in projects:
                # Add any values we don't already have
                existing_info = projects[project_name]
                for k, c in zip(headings, row):
                    new_value = c.value
                    if new_value is None:
                        continue
                    if existing_info[k] is None:
                        existing_info[k] = new_value
                    elif new_value != existing_info[k]:
                        print(u"Mismatched project info: '{0}' vs '{1}'".format(new_value, existing_info[k]))
                        # Use longest or biggest
                        try:
                            if len(new_value) > len(existing_info[k]):
                                existing_info[k] = new_value
                        except TypeError:
                            try:
                                if new_value > existing_info[k]:
                                    existing_info[k] = new_value
                            except TypeError:
                                pass
            else:
                # Add initial values
                projects[project_name] = {k: c.value for (k, c) in zip(headings, row)}
    return projects


def _get_project_dict_headings(heading_row):
    headings = list()
    for heading_cell in heading_row:
        if heading_cell.value is None:
            break
        headings.append(canonical(heading_cell.value.strip()))
    return headings


def load_cvs():
    cv_dicts = get_cv_dicts()
    for cv_dict in cv_dicts:
        try:
            cv = cm.CV.objects.get(slug=cv_dict['slug'])
        except cm.CV.DoesNotExist:
            cv = cm.CV()

        setup_user(cv_dict, cv)

        for (attname, key) in (('middle_names', 'Given Middle Name'),
                               ('alternate_names', 'Alternate Names Used'),
                               ('street', 'Mailing Address'),
                               ('city', 'City'),
                               ('state', 'State/Province'),
                               ('zip', 'ZIP/Postal Code'),
                               ('telephone', 'Telephone'),):
            setattr(cv, attname, cv_dict.get(key))

        # do the country fields together
        for (attname, key) in (('country', 'Country'),
                               ('citizenship', 'Citizenship'),
                               ('birth_country', 'Country of Birth')):
            country = get_country(cv_dict.get(key))
            if country:
                setattr(cv, attname, country)
            else:
                print("No country:", cv_dict['fname'], cv_dict.get(key))

        dob = cv_dict.get('Date of Birth')
        if type(dob) == datetime.datetime:
            cv.dob = dob

        # gender and marital status use the first letter of the relevant word in the field
        for (attname, key) in (('gender', 'Sex'),
                               ('marital_status', 'Marital Status')):
            value = cv_dict.get(key)
            if value:
                setattr(cv, attname, value[0].upper())

        cv.save()  # This must be done here so there is an entity to link related objects to

        for project_name, project_info in cv_dict['projects'].iteritems():
            cv_project = cm.CVProject()
            cv_project.project = pm.Project.objects.get(title=project_name)
            cv_project.cv = cv
            for (attname, key) in (
                    ('position', 'Position'),
                    ('person_months', 'Person-months'),
                    ('activities', 'Activities Performed'),
                    ('references', 'References')):
                setattr(cv_project, attname, project_info.get(key))
            cv_project.save()


def _get_country_by_field(s, field_name):
    kwargs = {field_name: s}
    try:
        return pm.Country.objects.get(**kwargs)
    except pm.Country.DoesNotExist:
        return None


def _get_country_by_name(s):
    s = canonical(s)
    return _get_country_by_field(s, 'name')


def _get_country_by_iso(s):
    # strip out any periods
    s = ''.join(s.split('.'))
    return _get_country_by_field(s, 'iso_3166')

country_names = pm.Country.objects.all().values_list('name', flat=True)


def _guess_country(s):
    try:
        country_name = next((country_name for country_name in country_names if country_name in s))
        return pm.Country.objects.get(name=country_name)
    except StopIteration:
        return None


def get_country(s):
    """
    Try to return a country matching s
    """
    if s:
        for f in (_get_country_by_name,
                  _get_country_by_iso,
                  _guess_country):
            country = f(s)
            if country:
                return country


def setup_user(cv_dict, cv):
    """
    Use existing user if available on cv object. If no user:
    Find an existing matching user or create one as necessary.
    """
    try:
        return cv.user
    except cm.User.DoesNotExist:

        for username in gen_username(cv_dict['Given First Name'], cv_dict.get('Surname')):
            try:
                if cm.CV.objects.get(user__username=username):
                    continue
            except cm.CV.DoesNotExist:
                break

        user, created = cm.User.objects.get_or_create(username=username)

        if created:
            user.set_password(u"{0}42why".format(username))
            user.first_name = cv_dict['Given First Name']
            user.last_name = cv_dict['Surname']
            if cv_dict.get('Email'):
                user.email = cv_dict['Email']
            user.save()

        cv.user = user

        return user


def gen_username(first_name, last_name=None, max_len=30):
    """
    Generate username candidates
    'Jo Ho' -> ['jo', 'joh', 'joho', 'jo1', 'jo2'...]
    """
    # TODO: This may duplicate integer suffixed usernames when cropping to max_len because the duplicate
    # may be ten earlier e.g:
    # [n for n in gen_username('a', '', max_len=2)] ->
    # ['a', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a1']

    if last_name is None:
        last_name = ''
    if max_len < 1:
        raise Exception('gen_username: max_len must be greater than zero')
    if len(first_name) < 1:
        raise Exception('gen_username: first_name length must be greater than zero')

    previous_name_stash = [None]  # Controls when to stop

    def build(first, second, previous_name_stash):
        len_first, len_second = len(first), len(second)
        reduction = max(0, (len_first + len_second) - max_len)
        first = first[0:max(1, len_first - reduction)]
        reduction = max(0, reduction - (len_first - 1))
        second = second[0:max(0, len_second - reduction)]

        new_name = first + second
        if new_name == previous_name_stash[0]:
            raise StopIteration
        previous_name_stash[0] = new_name
        return new_name

    first_name = first_name.lower()
    last_name = last_name.lower()

    yield build(first_name, '', previous_name_stash)
    for i in range(len(last_name)):
        yield build(first_name, last_name[0:i+1], previous_name_stash)
    i = 0
    while True:
        i += 1
        yield build(first_name, str(i), previous_name_stash)


def get_cv_dicts():
    cv_dicts = list()
    for cv in xlsx_cvs:
        try:
            wb = load_workbook(filename=cv)
        except TypeError:
            print("Unable to open {0}".format(cv))
            continue
        ws = wb.get_sheet_by_name('BIODATA')
        cv_dict = {canonical(row[0].value.strip()): row[1].value
                   for row in ws.rows if row[0].value is not None}
        # slug is not perfect (assumes no duplicate names)
        # but is needed here so we can update cvs effectively
        if 'Given First Name' in cv_dict:
            cv_dict['fname'] = cv
            cv_dict['slug'] = get_slug(cv_dict)
            cv_dict['projects'] = _get_project_dicts_from_wb(wb)
            cv_dicts.append(cv_dict)
        else:
            print("Skipped '{0}' - no given first name".format(cv))
    return cv_dicts


def get_slug(cv_dict):
    """
    emulates the cv model get_slug function with the dict data
    """
    return slugify(u"{0}-{1}-{2}".format(cv_dict["Given First Name"],
                                         cv_dict.get("Given Middle Name", ''),
                                         cv_dict.get("Surname", '')))

# synonyms map a synonym to a canonical value.
synonyms = {'Services On and Off-site': 'Services On/Off-site',
            'Given Name': 'Given First Name',
            'Given Second Name': 'Given Middle Name',
            'Date of Birth (mm/dd/yyyy)': 'Date of Birth',
            'Date of Birth (mm/dd/yy)': 'Date of Birth',
            'Family Name / Surname': 'Surname',
            '=HYPERLINK("http://en.wikipedia.org/wiki/ISO_3166-1", "Country")': 'Country',
            'UK (British)': 'United Kingdom',
            'French': 'France'}


def canonical(s):
    """
    Headings are not consistent across all CVS. Use canonical to eliminae the synonyms.
    """
    return synonyms.get(s, s)