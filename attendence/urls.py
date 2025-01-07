from django.urls import path
from . import views

urlpatterns = [
    path('mark/<str:emp_id>/', views.mark_attendance, name='mark_attendance'),
    path('daily-report/', views.daily_report, name='daily_report'),
    path('export-daily-report/', views.export_daily_report, name='export_daily_report'),
]
