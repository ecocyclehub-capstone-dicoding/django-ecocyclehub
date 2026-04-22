from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.users.models import User
from .serializers import RegisterSerializer
from apps.users.serializers import UserResponseSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user = User.objects.select_related("role").prefetch_related("role__permissions").get(id=user.id)

            response_serializer = UserResponseSerializer(user)

            return Response({
                "success": True,
                "message": "User registered successfully",
                "code": "201",
                "data": response_serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "message": "Validation error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
