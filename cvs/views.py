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


class ProjectListView(ListView):
    model = cm.Project

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['use_right_col'] = "No"
        context['categorization'] = categorize_projects(context['object_list'])
        return context


def categorize_projects(projects):
    """
    Organise the projects so that they are nested in the ifc theme labels
    """
    categorization = dict()
    for project in projects:
        theme_name = project.ifc_subtheme.theme.name
        subtheme_name = project.ifc_subtheme.name

        if theme_name not in categorization:
            categorization[theme_name] = dict(subthemes=dict(), count=0)

        if subtheme_name not in categorization[theme_name]['subthemes']:
            categorization[theme_name]['subthemes'][subtheme_name] = dict(projects=list(), count=0)

        categorization[theme_name]['count'] += 1
        categorization[theme_name]['id'] = project.ifc_subtheme.theme.id
        categorization[theme_name]['subthemes'][subtheme_name]['projects'].append(project)
        categorization[theme_name]['subthemes'][subtheme_name]['count'] += 1
        categorization[theme_name]['subthemes'][subtheme_name]['id'] = project.ifc_subtheme.id

    return categorization


