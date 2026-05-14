from django.db import transaction
from django.db.models import F
from django.utils import timezone
from apps.points.models import Point
from apps.balances.models import Balance

def update_user_balance_and_points(user, total_price, total_points):
    with transaction.atomic():
        point_obj, _ = Point.objects.get_or_create(
            user=user, defaults={"total_points": 0}
        )
        Point.objects.filter(pk=point_obj.pk).update(
            total_points=F("total_points") + total_points,
            updated_at=timezone.now()
        )

        balance_obj, _ = Balance.objects.get_or_create(
            user=user, defaults={"total_balance": 0}
        )
        Balance.objects.filter(pk=balance_obj.pk).update(
            total_balance=F("total_balance") + total_price,
            updated_at=timezone.now()
        )
