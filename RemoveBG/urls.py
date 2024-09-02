from django.urls import path
from . import views

urlpatterns = [
    path('', views.page_upload, name='index'),
    path('upload/', views.upload_file, name='upload_file'),
    path('contact/', views.contact_view, name='contact'),
    path('donwload/', views.download_file, name='download_file'),
    path('serve_file/<str:file_name>/', views.serve_file, name='serve_file'),
]