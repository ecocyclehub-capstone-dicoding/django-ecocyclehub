from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.points.models import Point
from common.responses import (
    format_success_response,
    format_error_response
)
from .models import Level
from .serializers import LevelSerializer
from .services import get_user_level

class LevelListCreateView(APIView):

    def get(self, request):
        levels = Level.objects.all()

        serializer = LevelSerializer(levels, many=True)

        return Response(
            format_success_response(
                "Levels retrieved successfully",
                serializer.data,
                200
            )
        )

    def post(self, request):
        serializer = LevelSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                format_success_response(
                    "Level created successfully",
                    serializer.data,
                    201
                ),
                status=status.HTTP_201_CREATED
            )

        return Response(
            format_error_response(
                "Validation error",
                serializer.errors,
                400
            ),
            status=status.HTTP_400_BAD_REQUEST
        )

class LevelDetailView(APIView):

    def put(self, request, pk):
        try:
            level = Level.objects.get(pk=pk)
        except Level.DoesNotExist:
            return Response(
                format_error_response(
                    "Resource not found",
                    None,
                    404
                ),
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = LevelSerializer(level, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                format_success_response(
                    "Level updated successfully",
                    serializer.data,
                    200
                )
            )

        return Response(
            format_error_response(
                "Validation error",
                serializer.errors,
                400
            ),
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        try:
            level = Level.objects.get(pk=pk)
        except Level.DoesNotExist:
            return Response(
                format_error_response(
                    "Resource not found",
                    None,
                    404
                ),
                status=status.HTTP_404_NOT_FOUND
            )

        level.delete()

        return Response(
            format_success_response(
                "Level deleted successfully",
                None,
                200
            )
        )

class LeaderboardView(APIView):

    def get(self, request):
        leaderboard = Point.objects.select_related(
            "user"
        ).order_by("-total_points")[:10]

        data = []

        for item in leaderboard:
            level = get_user_level(item.total_points)

            data.append({
                "name": item.user.name,
                "points": item.total_points,
                "level": level.name if level else None
            })

        return Response(
            format_success_response(
                "Leaderboard retrieved successfully",
                data,
                200
            )
        )
