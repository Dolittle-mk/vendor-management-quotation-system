from django.urls import path
from . import views

app_name = 'dashboard'  # This is important for reverse lookup

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
]