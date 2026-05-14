from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.models import User
from apps.balances.models import Balance
from apps.points.models import Point


@receiver(post_save, sender=User)
def create_user_balance_and_point(
    sender,
    instance,
    created,
    **kwargs
):
    if not created:
        return

    with transaction.atomic():
        Balance.objects.get_or_create(user=instance)
        Point.objects.get_or_create(user=instance)
