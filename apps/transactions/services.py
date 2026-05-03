from apps.points.models import Point
from apps.balances.models import Balance

def update_user_balance_and_points(user, total_price, total_points):
    # Points
    point_obj, _ = Point.objects.get_or_create(user=user)
    point_obj.total_points += total_points
    point_obj.save()

    # Balance
    balance_obj, _ = Balance.objects.get_or_create(user=user)
    balance_obj.total_balance += total_price
    balance_obj.save()
