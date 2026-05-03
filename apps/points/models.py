from django.db import models

class Point(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    total_points = models.PositiveIntegerField(default=0)
    update_at = models.DateTimeField(auto_now_add=True)
