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

class CategoryListCreateView(APIView):
    def get_permissions(self):
        permission_map = {
            'GET': CanViewCategory,
            'POST': CanAddCategory,
            'PUT': CanEditCategory,
            'DELETE': CanDeleteCategory,
        }

        permission_class = permission_map.get(self.request.method)
        return [permission_class()] if permission_class else []

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

class CategoryUpdateDeleteView(APIView):
    def get_permissions(self):
        permission_map = {
            'GET': CanViewCategory,
            'POST': CanAddCategory,
            'PUT': CanEditCategory,
            'DELETE': CanDeleteCategory,
        }

        permission_class = permission_map.get(self.request.method)
        return [permission_class()] if permission_class else []

    def put(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(
                format_error_response(
                    "Resource not found",
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

    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(
                format_error_response(
                    "Resource not found",
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
