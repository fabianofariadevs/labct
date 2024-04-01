import sys
sys.path.append('/Users/fabia/VsCodeProjects/labct24')

wsgi_app = 'labct.app:app'
bind = '0.0.0.0:5000'
workers = 4