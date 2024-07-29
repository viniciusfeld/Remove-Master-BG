from django.urls import path
from . import views

urlpatterns = [
    path('', views.page_upload, name='index'),
    path('upload/', views.upload_file, name='upload_file'),
    path('contact/', views.contact_view, name='contact'),
    # outras URLs
]