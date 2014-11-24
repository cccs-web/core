from django import template

register = template.Library()


def joinby(value, delim=', '):
    string_values = [u'{0}'.format(v) for v in value]
    return delim.join(string_values)

register.filter('join', joinby)

def cvproject_list(project):
    return project.cvproject_set.all()

register.filter('cvproject_list', cvproject_list)




