from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_csv, name='upload-csv'),
    path('datasets/list/', views.list_datasets, name='list-datasets'),
    path('datasets/<int:dataset_id>/', views.get_dataset, name='get-dataset'),
    path('datasets/<int:dataset_id>/delete/', views.delete_dataset, name='delete-dataset'),
    path('summary/<int:dataset_id>/', views.get_summary, name='get-summary'),
    path('summary/<int:dataset_id>/types/', views.get_type_stats, name='get-type-stats'),
    path('report/<int:dataset_id>/pdf/', views.generate_pdf_report, name='generate-pdf'),
]