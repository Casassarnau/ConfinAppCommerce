from django.db import models

from shop.models import Shop
from user.models import User


class Purchase(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='purchase')
    shop = models.ForeignKey(to=Shop, on_delete=models.DO_NOTHING, related_name='purchase')
    dateTime = models.DateTimeField()
