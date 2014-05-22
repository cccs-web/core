import os
import fabric.api as fab

from mezzanine.conf import settings


@fab.task
@fab.hosts(['localhost'])
def reset_cvs():
    """
    Reset the cvs data completely, recreating all the tables and importing the data.
    This is for development only!!!
    """
    venv_path = '/home/{0}/.virtualenvs'.format(fab.env.user)
    venv_bin = os.path.join(venv_path, settings.VIRTUALENV, 'bin')
    with fab.prefix("source {0}".format(os.path.join(venv_bin, "activate"))):
        with fab.prefix("source {0}".format(os.path.join(venv_bin, "postactivate"))):
            # Drop the existing database tables and recreate them
            with fab.settings(warn_only=True):  # Might have no tables
                cvs_tables = fab.run('psql -d cccs -c "SELECT tablename FROM pg_tables WHERE schemaname = \'public\';" | grep \'^ cvs_\'')
                cvs_tables += ' '
                cvs_tables += fab.run('psql -d cccs -c "SELECT tablename FROM pg_tables WHERE schemaname = \'public\';" | grep \'^ projects_\'')
            for cvs_table in cvs_tables.split():
                fab.run('psql -d cccs -c "DROP TABLE IF EXISTS {0} CASCADE;"'.format(cvs_table))
            fab.run('django-admin.py syncdb')  # rebuild the empty database tables