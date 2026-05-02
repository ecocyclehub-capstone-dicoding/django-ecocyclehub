from django.urls import path
from .views import (
    CategoryCreateView,
    CategoryListView,
    CategoryUpdateView,
    CategoryDeleteView
)

urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'),
    path('', CategoryCreateView.as_view(), name='category-create'),
    path('<uuid:pk>/', CategoryUpdateView.as_view(), name='category-update'),
    path('<uuid:pk>/', CategoryDeleteView.as_view(), name='category-delete'),
]
