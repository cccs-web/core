import os

from bs4 import BeautifulSoup

from django.conf import settings


class ProjectException(Exception):
    pass


class QGISProject(object):
    """
    Object representing a QGIS project.
    """
    def __init__(self, project_name):

        if settings.QGIS_PROJECTS_DIR in project_name:  # reduce it to just the project_name
            project_name = project_name[len(settings.QGIS_PROJECTS_DIR) + 1:]
        self.name = project_name

        with open(self.filepath, 'rb') as f:
            soup = BeautifulSoup(f, 'xml')
            self.title = soup.title.string
            self.qgis_project_name = soup.qgis['projectname']

    @property
    def filepath(self):
        """
        :return: full path to the project qgs file
        """
        project_dir = os.path.join(settings.QGIS_PROJECTS_DIR, self.name)
        qgs_files = [file_name for file_name in os.listdir(project_dir) if file_name.lower()[-3:] == 'qgs']

        if not qgs_files:
            raise ProjectException('No qgs file in {project_dir}'.format(project_dir=project_dir))
        if qgs_files[1:]:
            raise ProjectException('More than one qgs file in {project_dir}'.format(project_dir=project_dir))

        return os.path.join(project_dir, qgs_files[0])

    @property
    def url(self):
        """
        :return: absolute url to the project server that returns this project
        """
        return settings.QGIS_SERVER_URL_PATTERN.format(
            file_path=self.filepath)


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
    result.sort(key=lambda x: x.name)
    return result
