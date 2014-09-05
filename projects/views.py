from collections import OrderedDict

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core import serializers

import projects.models as pm


class CCCSDetailView(DetailView):

    def get_context_data(self, **kwargs):
        context = super(CCCSDetailView, self).get_context_data(**kwargs)
        context['serialized'] = serializers.serialize('python', [self.get_object()])[0]
        return context


class ProjectDetailView(CCCSDetailView):
    model = pm.Project

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['cvproject_list'] = self.get_object().cvproject_set.all()
        return context


class ProjectCCCSThemeListView(ListView):
    model = pm.Project
    categorization_fieldname = 'cccs_subthemes'
    categorization_parent_fieldname = 'theme'
    categorization_label = 'CCCS Theme'
    template_name = "projects/project_list2.html"

    def get_context_data(self, **kwargs):
        context = super(ProjectCCCSThemeListView, self).get_context_data(**kwargs)
        context['categorization_name'] = self.categorization_label
        context['use_right_col'] = "No"  # a bit hacky but it will do for now
        context['categorization'] = categorize_projects2(context['object_list'],
                                                         self.categorization_fieldname,
                                                         self.categorization_parent_fieldname,
                                                         not self.request.user.is_staff)
        return context


class ProjectIFCThemeListView(ProjectCCCSThemeListView):
    categorization_fieldname = 'ifc_subthemes'
    categorization_label = 'IFC Performance Standard'


class ProjectCCCSSectorListView(ProjectCCCSThemeListView):
    categorization_fieldname = 'cccs_subsectors'
    categorization_parent_fieldname = 'sector'
    categorization_label = 'CCCS Sector'


class ProjectCCCSSubSectorListView(ListView):
    model = pm.Project
    template_name = "projects/project_cccs_sub_list.html"

    def get_context_data(self, **kwargs):
        context = super(ProjectCCCSSubSectorListView, self).get_context_data(**kwargs)
        sub = pm.CCCSSubSector.objects.get(pk=int(self.kwargs['pk']))
        context['sub'] = sub
        projects = pm.Project.objects.filter(cccs_subsectors=sub)
        if not self.request.user.is_staff:
            projects = projects.filter(status=pm.CONTENT_STATUS_PUBLISHED)
        context['projects'] = projects
        return context


class ProjectCCCSSectorExperienceView(ProjectCCCSThemeListView):
    categorization_fieldname = 'cccs_subsectors'
    categorization_parent_fieldname = 'sector'
    categorization_label = 'CCCS Sector'
    template_name = "projects/cccs_sector_experience.html"

    def get_context_data(self, **kwargs):
        context = super(ProjectCCCSSectorExperienceView, self).get_context_data(**kwargs)
        # Create a roughly equal pair of columns for the categorization
        categorization = context['categorization']
        categorization_cols = (OrderedDict(), OrderedDict())

        def next_col():
            while True:
                yield 0
                yield 1
        col = next_col()
        for super_name in categorization:
            categorization_cols[col.next()][super_name] = categorization[super_name]
        context['categorization_cols'] = categorization_cols
        return context


class ProjectCountryListView(ListView):
    model = pm.Project
    categorization_fieldname = 'countries'
    categorization_label = 'Country'
    template_name = "projects/project_list1.html"

    def get_context_data(self, **kwargs):
        context = super(ProjectCountryListView, self).get_context_data(**kwargs)
        context['categorization_name'] = self.categorization_label
        context['use_right_col'] = "No"  # a bit hacky but it will do for now
        context['categorization'] = categorize_projects(context['object_list'],
                                                        self.categorization_fieldname,
                                                        not self.request.user.is_staff)
        return context


class ProjectIFCSectorListView(ProjectCountryListView):
    categorization_fieldname = 'ifc_sectors'
    categorization_label = 'IFC Sector'


class ProjectCCCSProjectListView(ListView):
    model = pm.Project
    template_name = "projects/cccs_project_list.html"

    def get_queryset(self):
        qs = super(ProjectCCCSProjectListView, self).get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(status=pm.CONTENT_STATUS_PUBLISHED)
        return qs.filter(tags__name__in=['CCCS'])


def categorize_projects(projects, categorization_fieldname, published_only):
    """
    Organise the projects using a single categorization layer
    """
    categorization = dict()
    for project in projects:
        if published_only and project.status == pm.CONTENT_STATUS_DRAFT:
            continue
        categories = getattr(project, categorization_fieldname).all()
        for category in categories:
            category_name = category.name
            if category_name not in categorization:
                categorization[category_name] = dict(projects=list(), count=0)
            categorization[category_name]['count'] += 1
            categorization[category_name]['id'] = category.id
            categorization[category_name]['projects'].append(project)
    return OrderedDict(((k, categorization[k]) for k in sorted(categorization.keys())))


def categorize_projects2(projects, categorization_fieldname, categorization_parent_fieldname, published_only):
    """
    Organise the projects so that they are nested in the sub categorizations
    """
    categorization = dict()
    for project in projects:
        if published_only and project.status == pm.CONTENT_STATUS_DRAFT:
            continue
        sub_categorizations = getattr(project, categorization_fieldname).all()

        for sub in sub_categorizations:
            sub_name = sub.name
            super_name = getattr(sub, categorization_parent_fieldname).name

            if super_name not in categorization:
                categorization[super_name] = dict(subs=dict(), count=0)

            if sub_name not in categorization[super_name]['subs']:
                categorization[super_name]['subs'][sub_name] = dict(projects=list(), count=0)

            categorization[super_name]['count'] += 1
            categorization[super_name]['id'] = getattr(sub, categorization_parent_fieldname).id
            categorization[super_name]['subs'][sub_name]['projects'].append(project)
            categorization[super_name]['subs'][sub_name]['count'] += 1
            categorization[super_name]['subs'][sub_name]['id'] = sub.id

    for info in categorization.values():
        info['subs'] = OrderedDict(((k, info['subs'][k]) for k in sorted(info['subs'].keys())))
    return OrderedDict(((k, categorization[k]) for k in sorted(categorization.keys())))