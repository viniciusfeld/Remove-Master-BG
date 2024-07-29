from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_view, name='index'),
    path('upload/', views.upload_file, name='upload_file'),
    # outras URLs
]