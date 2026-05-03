from django.urls import path
from .views import (
    CustomerDashboardView,
    OfficerDashboardView,
    AdminDashboardView
)

urlpatterns = [
    path('customers/', CustomerDashboardView.as_view()),
    path('officer/', OfficerDashboardView.as_view()),
    path('admin/', AdminDashboardView.as_view()),
]
