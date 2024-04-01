import sys
sys.path.append('/Users/fabia/VsCodeProjects/labct24/labct')

wsgi_app = 'labct.app:app'
bind = '0.0.0.0:8080'
workers = 4