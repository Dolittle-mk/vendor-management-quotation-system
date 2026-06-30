from django.urls import path
from . import views

app_name = 'vendors'

urlpatterns = [
    path('', views.vendor_list, name='vendor_list'),
    path('create/', views.vendor_create, name='vendor_create'),
    path('<int:pk>/', views.vendor_detail, name='vendor_detail'),
    path('<int:pk>/update/', views.vendor_update, name='vendor_update'),
    path('<int:pk>/delete/', views.vendor_delete, name='vendor_delete'),
]