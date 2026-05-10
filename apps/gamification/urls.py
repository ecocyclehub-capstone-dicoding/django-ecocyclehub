from django.urls import path

from .views import (
    LeaderboardView,
    LevelListCreateView,
    LevelDetailView
)

urlpatterns = [
    path("leaderboard/", LeaderboardView.as_view(), name='leaderboard'),
    path("levels/", LevelListCreateView.as_view(), name='level-list'),
    path("levels/<uuid:pk>/", LevelDetailView.as_view(), name='level-detail'),
]
