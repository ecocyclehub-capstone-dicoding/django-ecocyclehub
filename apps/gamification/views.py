from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.points.models import Point
from common.exceptions import handle_serializer_error
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
            ),
            status=status.HTTP_200_OK
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

        error = handle_serializer_error(serializer.errors)

        return Response(
            error["response"],
            status=error["status"]
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
                ),
                status=status.HTTP_200_OK
            )

        error = handle_serializer_error(serializer.errors)

        return Response(
            error["response"],
            status=error["status"]
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
            ),
            status=status.HTTP_200_OK
        )

class LeaderboardView(APIView):

    def get(self, request):
        limit = request.query_params.get("limit", 10)

        leaderboard = Point.objects.select_related(
            "user"
        ).order_by(
            "-total_points",
            "user__created_at"
        )[:int(limit)]

        data = []

        for index, item in enumerate(leaderboard, start=1):
            level = get_user_level(item.total_points)

            data.append({
                "rank": index,
                "user": {
                    "id": item.user.id,
                    "name": item.user.name,
                    "email": item.user.email
                },
                "points": item.total_points,
                "level": (
                    LevelSerializer(level).data
                    if level else None
                )
            })

        return Response(
            format_success_response(
                "Leaderboard retrieved successfully",
                data,
                200
            ),
            status=status.HTTP_200_OK
        )
