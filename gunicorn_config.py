import sys
sys.path.append('/home/ubuntu/labct24')

wsgi_app = 'app:app'
bind = '0.0.0.0:5000'
workers = 4