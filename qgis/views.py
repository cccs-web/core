import os

from bs4 import BeautifulSoup

from django.conf import settings
from django.views.generic import TemplateView


class QGISProject(object):
    """
    Object representing a QGIS project, created using qgs file.
    """
    def __init__(self, file_name):
        self.file_name = file_name
        default_name = os.path.splitext(file_name)[0].capitalize()
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
        return [QGISProject(fn) for fn in os.listdir(settings.QGIS_PROJECTS_DIR)
                if os.path.splitext(fn)[1] == '.qgs']



