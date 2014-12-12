import os

from bs4 import BeautifulSoup

from django.conf import settings
from django.views.generic import TemplateView


class QGISProject(object):
    """
    Object representing a QGIS project, created using qgs file.
    """
    def __init__(self, file_name):

        if settings.QGIS_PROJECTS_DIR in file_name:
            file_name = file_name[len(settings.QGIS_PROJECTS_DIR) + 1:]
        self.file_name = file_name

        default_name = os.path.splitext(os.path.basename(file_name))[0].capitalize()
        with open(os.path.join(settings.QGIS_PROJECTS_DIR, file_name), 'rb') as f:
            soup = BeautifulSoup(f, 'xml')
            self.title = soup.title.string if soup.title.string else default_name
            self.name = soup.qgis['projectname'] if soup.qgis['projectname'] else default_name


class HomeView(TemplateView):
    """
    Specialization to provide information about the projects
    """
    template_name = "qgis/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['projects'] = self.get_projects()
        return context

    @staticmethod
    def get_projects():
        """
        :return: list of QGIS Project objects
        """

        result = list()
        for dirpath, dirnames, filenames in os.walk(settings.QGIS_PROJECTS_DIR):
            for fn in filenames:
                if os.path.splitext(fn)[1] == '.qgs':
                    file_name = os.path.join(dirpath, fn)
                    result.append(QGISProject(file_name))
        result.sort(key=lambda x: x.name)
        return result


class QGISProjectView(TemplateView):
    """
    Specialization to inject project data for javascript
    """
    template_name = "qgis/project.html"

    def get_context_data(self, **kwargs):
        context = super(QGISProjectView, self).get_context_data(**kwargs)
        context['file_name'] = self.kwargs['file_name']
        context['qgis_server_url'] = settings.QGIS_SERVER_URL
        return context




