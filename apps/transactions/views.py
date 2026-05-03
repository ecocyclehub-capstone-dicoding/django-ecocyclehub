from django.db import transaction as db_transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.transactions.models import Transaction
from common.responses import format_success_response, format_error_response
from common.exceptions import handle_serializer_error
from apps.permissions.custom_permissions import (
    CanViewTransaction,
    CanCreateTransaction,
    CanVerifyTransaction
)
from apps.transactions.services import update_user_balance_and_points
from .serializers import TransactionCreateSerializer, TransactionSerializer

class TransactionListCreateView(APIView):
    def get_permissions(self):
        permission_map = {
            'GET': CanViewTransaction,
            'POST': CanCreateTransaction,
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

class TransactionVerifyView(APIView):
    permission_classes = [CanVerifyTransaction]

    def post(self, request, pk):
        try:
            with db_transaction.atomic():
                transaction = (
                    Transaction.objects.select_for_update()
                    .select_related("user")
                    .get(pk=pk)
                )

                if transaction.status == "verified":
                    return Response(
                        format_error_response("Transaction already verified", None, 400),
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                transaction.status = "verified"
                transaction.handled_by = request.user
                transaction.verified_by = request.user
                transaction.save(update_fields=["status", "handled_by", "verified_by"])

                update_user_balance_and_points(
                    user=transaction.user,
                    total_price=transaction.total_price,
                    total_points=transaction.total_points,
                )
        except Transaction.DoesNotExist:
            return Response(
                format_error_response("Resource not found", None, 404),
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            format_success_response(
                "Transaction verified successfully",
                {
                    "id": transaction.id,
                    "status": transaction.status
                },
                200
            ),
            status=status.HTTP_200_OK
        )
