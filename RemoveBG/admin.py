from django.contrib import admin
from Master.settings import BASE_DIR

# Register your models here.

admin.site.login_template = f'{BASE_DIR}/RemoveBG/templates/registration/login.html'