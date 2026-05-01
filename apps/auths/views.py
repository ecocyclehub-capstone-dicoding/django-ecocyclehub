from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from apps.permissions.serializers import RoleSerializer
from apps.users.serializers import UserResponseSerializer
from apps.users.models import User
from common.responses import format_error_response
from .serializers import RegisterSerializer, LoginSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user = (
                User.objects
                .select_related("role")
                .prefetch_related("role__permissions")
                .get(id=user.id)
            )

            response_serializer = UserResponseSerializer(user)

            return Response({
                "success": True,
                "message": "User registered successfully",
                "code": "201",
                "data": response_serializer.data
            }, status=status.HTTP_201_CREATED)

        errors = serializer.errors

        # Check for "required" error codes
        is_required_error = any(
            getattr(err, 'code', None) == 'required'
            for field_errors in errors.values()
            for err in field_errors
        )


        if is_required_error:
            return Response(
                format_error_response(
                    "Some required fields are missing",
                    errors,
                    422
                ),
                status=422
            )

        return Response(
            format_error_response(
                "Validation error",
                errors,
                400
            ),
            status=400
        )

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            user = serializer.validated_data["user"]

            refresh = RefreshToken.for_user(user)

            user = (
                User.objects
                .select_related("role")
                .prefetch_related("role__permissions")
                .get(id=user.id)
            )

            return Response({
                "success": True,
                "message": "User login successfully",
                "code": "200",
                "data": {
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                    "role": RoleSerializer(user.role).data if user.role else None
                }
            })

        return Response({
            "success": False,
            "message": "Invalid credentials",
            "code": "401",
            "errors": serializer.errors
        }, status=status.HTTP_401_UNAUTHORIZED)

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            return Response({
                "success": True,
                "message": "Token refreshed successfully",
                "code": "200",
                "data": {
                    "access_token": response.data.get("access")
                }
            })

        return Response({
            "success": False,
            "message": "Invalid refresh token",
            "code": "401",
            "errors": response.data
        }, status=status.HTTP_401_UNAUTHORIZED)
