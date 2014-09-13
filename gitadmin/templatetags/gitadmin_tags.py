import subprocess

from django import template

register = template.Library()


def git_dashboard():
    return {
        'status': get_git_status()
    }


def get_git_status():
    """
    Return git status - run a fetch first so that the result is potentially useful
    :return: git status output as a string
    """
    if subprocess.call(['git', 'fetch']) != 0:
        return 'Unable to access GitHub!'
    p = subprocess.Popen(['git', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdoutdata, stderrdata = p.communicate()
    if stderrdata:
        stdoutdata += '\n' + stderrdata
    return stdoutdata

register.inclusion_tag('gitadmin/dashboard.html')(git_dashboard)