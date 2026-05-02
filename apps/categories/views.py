from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from common.exceptions import handle_serializer_error
from common.responses import format_error_response, format_success_response
from apps.permissions.custom_permissions import (
    CanAddCategory,
    CanViewCategory,
    CanEditCategory,
    CanDeleteCategory
)
from .serializers import CategorySerializer
from .models import Category

class CategoryCreateView(APIView):
    permission_classes = [CanAddCategory]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            category = serializer.save()
            return Response(
                format_success_response(
                    "Data created successfully",
                    CategorySerializer(category).data,
                    201
                ),
                status=status.HTTP_201_CREATED
            )

        error = handle_serializer_error(serializer.errors)

        return Response(
            error["response"],
            status=error["status"]
        )

class CategoryListView(APIView):
    permission_classes = [CanViewCategory]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)

        return Response(
            format_success_response(
                "Data retrieved successfully",
                serializer.data,
                200
            ),
            status=status.HTTP_200_OK
        )

class CategoryUpdateView(APIView):
    permission_classes = [CanEditCategory]

    def put(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(
                format_error_response(
                    "Resources not found",
                    None,
                    404
                ), status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, data=request.data)

        if serializer.is_valid():
            category = serializer.save()
            return Response(
                format_success_response(
                    "Data updated successfully",
                    CategorySerializer(category).data,
                    200
                ),
                status=status.HTTP_200_OK
            )

        error = handle_serializer_error(serializer.errors)

        return Response(
            error["response"],
            status=error["status"]
        )

class CategoryDeleteView(APIView):
    permission_classes = [CanDeleteCategory]

    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(
                format_error_response(
                    "Resources not found",
                    None,
                    404
                ), status=status.HTTP_404_NOT_FOUND)

        category.delete()

        return Response(
            format_success_response(
                "Data deleted successfully",
                None,
                200
            ), status=status.HTTP_200_OK)
