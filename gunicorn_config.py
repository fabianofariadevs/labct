import sys
sys.path.append('/home/ubuntu/labct')

wsgi_app = 'labct.app:app'
bind = '0.0.0.0:5000'
workers = 4