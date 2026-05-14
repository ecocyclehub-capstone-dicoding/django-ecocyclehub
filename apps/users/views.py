from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from common.exceptions import handle_serializer_error
from common.responses import (
    format_error_response,
    format_success_response
)

from apps.permissions.custom_permissions import (
    CanAddUser,
    CanViewUser,
    CanEditUser,
    CanDeleteUser
)

from .models import User
from .serializers import (
    UserSerializer,
    UserResponseSerializer
)


class UserListCreateView(APIView):
    def get_permissions(self):
        permission_map = {
            'GET': CanViewUser,
            'POST': CanAddUser,
            'PUT': CanEditUser,
            'DELETE': CanDeleteUser,
        }

        permission_class = permission_map.get(self.request.method)

        return [permission_class()] if permission_class else []

    def get(self, request):
        users = User.objects.select_related("role").all()

        serializer = UserResponseSerializer(users, many=True)

        return Response(
            format_success_response(
                "Data retrieved successfully",
                serializer.data,
                200
            ),
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response(
                format_success_response(
                    "Data created successfully",
                    UserResponseSerializer(user).data,
                    201
                ),
                status=status.HTTP_201_CREATED
            )

        error = handle_serializer_error(serializer.errors)

        return Response(
            error["response"],
            status=error["status"]
        )


class UserDetailView(APIView):
    def get_permissions(self):
        permission_map = {
            'GET': CanViewUser,
            'POST': CanAddUser,
            'PUT': CanEditUser,
            'DELETE': CanDeleteUser,
        }

        permission_class = permission_map.get(self.request.method)

        return [permission_class()] if permission_class else []

    def get_object(self, pk):
        try:
            return User.objects.select_related("role").get(pk=pk)
        except User.DoesNotExist:
            return None

    def get(self, request, pk):
        user = self.get_object(pk)

        if not user:
            return Response(
                format_error_response(
                    "Resource not found",
                    None,
                    404
                ),
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserResponseSerializer(user)

        return Response(
            format_success_response(
                "Data retrieved successfully",
                serializer.data,
                200
            ),
            status=status.HTTP_200_OK
        )

    def put(self, request, pk):
        user = self.get_object(pk)

        if not user:
            return Response(
                format_error_response(
                    "Resource not found",
                    None,
                    404
                ),
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            updated_user = serializer.save()

            return Response(
                format_success_response(
                    "Data updated successfully",
                    UserResponseSerializer(updated_user).data,
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
        user = self.get_object(pk)

        if not user:
            return Response(
                format_error_response(
                    "Resource not found",
                    None,
                    404
                ),
                status=status.HTTP_404_NOT_FOUND
            )

        user.delete()

        return Response(
            format_success_response(
                "Data deleted successfully",
                None,
                200
            ),
            status=status.HTTP_200_OK
        )
