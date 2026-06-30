from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', accounts_views.home, name='home'), 
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('vendors/', include('vendors.urls')),
    path('quotations/', include('quotations.urls')),
]