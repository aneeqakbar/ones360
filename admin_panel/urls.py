from django.urls import path
from . import views

app_name = "admin_panel"

urlpatterns = [
    path("dashboard/", views.DashboardView.as_view(), name="DashboardView"),
]