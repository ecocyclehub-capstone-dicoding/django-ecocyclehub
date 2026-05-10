from .models import Level


def get_user_level(total_points):
    return Level.objects.filter(
        min_points__lte=total_points
    ).order_by("-min_points").first()
