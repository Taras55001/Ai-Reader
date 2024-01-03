
from django.urls import include,path

from . import views

app_name = 'pdf'

urlpatterns = [
    path('upload/', views.FileFieldFormView.as_view(), name='upload_file'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('delete_file/<int:file_id>/', views.delete_file, name='delete_file'),
]