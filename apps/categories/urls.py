from django.urls import path
from .views import (
    CategoryListCreateView,
    CategoryUpdateDeleteView,
)

urlpatterns = [
    path('', CategoryListCreateView.as_view(), name='category-list'),
    path('<uuid:pk>/', CategoryUpdateDeleteView.as_view(), name='category-detail'),
]
