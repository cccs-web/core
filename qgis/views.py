from django.conf import settings
from django.views.generic import TemplateView

import qgis.qgis_project as qp


class HomeView(TemplateView):
    """
    Specialization to provide information about the projects
    """
    template_name = "qgis/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['projects'] = qp.get_projects()
        return context


class QGISProjectView(TemplateView):
    """
    Specialization to inject project data for javascript
    """
    template_name = "qgis/project.html"

    def get_context_data(self, **kwargs):
        context = super(QGISProjectView, self).get_context_data(**kwargs)
        context['project'] = qp.QGISProject(self.kwargs['project_name'])
        return context




