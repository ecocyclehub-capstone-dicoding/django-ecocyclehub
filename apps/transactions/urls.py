from django.urls import path
from .views import TransactionListCreateView, TransactionVerifyView, TransactionManagementView

urlpatterns = [
    path('', TransactionListCreateView.as_view(), name='transaction-list'),
    path('<uuid:pk>/verify/', TransactionVerifyView.as_view(), name='transaction-verify'),
    path('all/',TransactionManagementView.as_view(),name='transaction-management-list'),
    path('all/<uuid:pk>/',TransactionManagementView.as_view(),name='transaction-management-detail'),
]
