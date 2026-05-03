from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.transactions.models import Transaction
from common.responses import format_success_response
from common.exceptions import handle_serializer_error
import apps.permissions.custom_permissions
from .serializers import TransactionCreateSerializer, TransactionSerializer

class TransactionListCreateView(APIView):
    def get_permissions(self):
        permission_map = {
            'GET': apps.permissions.custom_permissions.CanViewTransaction,
            'POST': apps.permissions.custom_permissions.CanCreateTransaction,
        }

        permission_class = permission_map.get(self.request.method)
        return [permission_class()] if permission_class else []

    def post(self, request):
        serializer = TransactionCreateSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            transaction = serializer.save()

            return Response(
                format_success_response(
                    "Transaction created successfully",
                    TransactionSerializer(transaction).data,
                    201
                ),
                status=status.HTTP_201_CREATED
            )

        error = handle_serializer_error(serializer.errors)

        return Response(error["response"], status=error["status"])

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user)

        serializer = TransactionSerializer(transactions, many=True)

        return Response(
            format_success_response(
                "Transaction retrieved successfully",
                serializer.data,
                200
            )
        )
