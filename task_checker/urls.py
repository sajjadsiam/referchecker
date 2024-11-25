# task_checker/urls.py
from django.contrib import admin
from django.urls import path
from analysis.views import analyze_wallets

urlpatterns = [
    path('admin/', admin.site.urls),
    path('analyze/', analyze_wallets, name='analyze_wallets'),
]