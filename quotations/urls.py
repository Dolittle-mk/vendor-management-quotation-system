from django.urls import path
from . import views

app_name = 'quotations'

urlpatterns = [
    path('', views.quotation_list, name='quotation_list'),
    path('create/', views.quotation_create, name='quotation_create'),
    path('<int:pk>/', views.quotation_detail, name='quotation_detail'),
    path('<int:pk>/update/', views.quotation_update, name='quotation_update'),
    path('<int:pk>/delete/', views.quotation_delete, name='quotation_delete'),
    path('<int:pk>/response/', views.quotation_response, name='quotation_response'),
    path('<int:pk>/history/', views.quotation_history, name='quotation_history'),
    path('compare/', views.quotation_compare, name='quotation_compare'),
]