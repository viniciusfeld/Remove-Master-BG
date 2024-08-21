import os
import sys

sys.path.insert(0, '/home/masterremovebg/apps_wsgi/Remove-Master-BG')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Master.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()