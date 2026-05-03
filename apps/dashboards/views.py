from django.db.models import Sum
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.transactions.models import Transaction
from apps.points.models import Point
from apps.balances.models import Balance
from apps.users.models import User
from common.responses import format_success_response
from apps.permissions.custom_permissions import (
    CanViewCustomerDashboard,
    CanViewOfficerDashboard,
    CanViewAdminDashboard
)


class CustomerDashboardView(APIView):
    permission_classes = [CanViewCustomerDashboard]

    def get(self, request):
        user = request.user

        # total points
        point_obj = Point.objects.filter(user=user).first()
        total_points = point_obj.total_points if point_obj else 0

        # total balance
        balance_obj = Balance.objects.filter(user=user).first()
        total_balance = balance_obj.total_balance if balance_obj else 0

        # transactions
        transactions = Transaction.objects.filter(user=user)

        total_transactions = transactions.count()

        # recent 5
        recent_transactions = transactions.order_by('-created_at')[:5]

        recent_data = [
            {
                "id": t.id,
                "total_price": t.total_price,
                "total_points": t.total_points,
                "status": t.status,
                "created_at": t.created_at
            }
            for t in recent_transactions
        ]

        return Response(
            format_success_response(
                "Customer dashboard retrieved",
                {
                    "total_points": total_points,
                    "total_balance": total_balance,
                    "total_transactions": total_transactions,
                    "recent_transactions": recent_data
                },
                200
            ),
            status=status.HTTP_200_OK
        )

class OfficerDashboardView(APIView):
    permission_classes = [CanViewOfficerDashboard]

    def get(self, request):
        user = request.user

        # pending
        pending_count = Transaction.objects.filter(status="pending").count()

        # verified today
        today = now().date()
        verified_today = Transaction.objects.filter(
            status="verified",
            created_at__date=today
        ).count()

        # handled by this officer
        handled_count = Transaction.objects.filter(
            handled_by=user
        ).count()

        return Response(
            format_success_response(
                "Officer dashboard retrieved",
                {
                    "pending_transactions": pending_count,
                    "verified_today": verified_today,
                    "handled_by_me": handled_count
                },
                200
            )
        )

class AdminDashboardView(APIView):
    permission_classes = [CanViewAdminDashboard]

    def get(self, request):

        total_users = User.objects.count()

        transactions = Transaction.objects.all()

        total_transactions = transactions.count()

        totals = transactions.aggregate(
            total_weight=Sum("total_weight"),
            total_points=Sum("total_points"),
            total_price=Sum("total_price"),
        )
        total_weight = totals["total_weight"] or 0
        total_points = totals["total_points"] or 0
        total_balance = totals["total_price"] or 0

        return Response(
            format_success_response(
                "Admin dashboard retrieved",
                {
                    "total_users": total_users,
                    "total_transactions": total_transactions,
                    "total_weight": total_weight,
                    "total_points": total_points,
                    "total_balance": total_balance
                },
                200
            )
        )
