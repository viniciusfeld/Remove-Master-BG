import os
import sys

sys.path.insert(0, '/home/seu_usuario/www/seu_projeto')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seu_projeto.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()