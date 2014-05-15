from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core import serializers

import cvs.models as cm


class ProjectDetailView(DetailView):
    model = cm.Project

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['serialized'] = serializers.serialize('python', [self.get_object()])[0]
        return context


class ProjectCCCSThemeListView(ListView):
    model = cm.Project
    categorization_fieldname = 'cccs_subthemes'
    categorization_parent_fieldname = 'theme'
    categorization_label = 'CCCS Theme'

    def get_context_data(self, **kwargs):
        context = super(ProjectCCCSThemeListView, self).get_context_data(**kwargs)
        context['categorization_name'] = self.categorization_label
        context['use_right_col'] = "No"  # a bit hacky but it will do for now
        context['categorization'] = categorize_projects(context['object_list'],
                                                        self.categorization_fieldname,
                                                        self.categorization_parent_fieldname)
        return context


class ProjectIFCThemeListView(ProjectCCCSThemeListView):
    categorization_fieldname = 'ifc_subthemes'
    categorization_label = 'IFC Theme'


class ProjectCCCSSectorListView(ProjectCCCSThemeListView):
    categorization_fieldname = 'cccs_subsectors'
    categorization_parent_fieldname = 'sector'
    categorization_label = 'CCCS Sector'


def categorize_projects(projects, categorization_fieldname, categorization_parent_fieldname):
    """
    Organise the projects so that they are nested in the ifc theme labels
    """
    categorization = dict()
    for project in projects:
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

    return categorization


