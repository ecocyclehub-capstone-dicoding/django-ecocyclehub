from django.urls import path
from .views import TransactionListCreateView, TransactionVerifyView

urlpatterns = [
    path('', TransactionListCreateView.as_view(), name='transaction-list'),
    path('<uuid:pk>/verify/', TransactionVerifyView.as_view(), name='transaction-verify'),
]
