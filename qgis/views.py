import os

from bs4 import BeautifulSoup

from django.conf import settings
from django.views.generic import TemplateView


class ProjectException(Exception):
    pass


class QGISProject(object):
    """
    Object representing a QGIS project, created using qgs file.
    """
    def __init__(self, project_name):

        if settings.QGIS_PROJECTS_DIR in project_name:  # reduce it to just the project_name
            project_name = project_name[len(settings.QGIS_PROJECTS_DIR) + 1:]
        self.project_name = project_name

        with open(self.qgs_filename, 'rb') as f:
            soup = BeautifulSoup(f, 'xml')
            self.title = soup.title.string
            self.qgis_project_name = soup.qgis['projectname']

    @property
    def qgs_filename(self):
        project_dir = os.path.join(settings.QGIS_PROJECTS_DIR, self.project_name)
        qgs_files = [file_name for file_name in os.listdir(project_dir) if file_name.lower()[-3:] == 'qgs']

        if not qgs_files:
            raise ProjectException('No qgs file in {project_dir}'.format(project_dir=project_dir))
        if qgs_files[1:]:
            raise ProjectException('More than one qgs file in {project_dir}'.format(project_dir=project_dir))

        return os.path.join(project_dir, qgs_files[0])


class HomeView(TemplateView):
    """
    Specialization to provide information about the projects
    """
    template_name = "qgis/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['projects'] = self.get_projects()
        context['qgis_server_url'] = settings.QGIS_SERVER_URL_ROOT
        return context

    @staticmethod
    def get_projects():
        """
        :return: list of QGIS Project objects obtained by reviewing QGIS_PROJECTS_DIR
        """

        result = list()
        for project_name in os.listdir(settings.QGIS_PROJECTS_DIR):
            try:
                result.append(QGISProject(project_name))
            except (OSError, ProjectException):
                continue
        result.sort(key=lambda x: x.project_name)
        return result


class QGISProjectView(TemplateView):
    """
    Specialization to inject project data for javascript
    """
    template_name = "qgis/project.html"

    def get_context_data(self, **kwargs):
        context = super(QGISProjectView, self).get_context_data(**kwargs)
        context['project_name'] = self.kwargs['project_name']
        context['qgis_server_url'] = settings.QGIS_SERVER_URL_ROOT + self.kwargs['project_name']
        return context




