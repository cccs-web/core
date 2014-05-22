import os

__ALL__ = ['xlsx_cvs', 'xlsx_cv']

pwd = os.path.dirname(__file__)
xlsx_cvs = [os.path.abspath(os.path.join(pwd, '../projects/source_data', fn))
            for fn in os.listdir(os.path.join(pwd, '../projects/source_data'))
            if fn.startswith('CV')]

xlsx_cv = next((cv for cv in xlsx_cvs if 'Aaron' in cv))