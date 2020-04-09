import uuid

from django.db import models

from shop.models import Shop
from user.models import User


PCH_STATUS = {
    ('P', 'Pending'),
    ('A', 'Accepted'),
    ('E', 'Expired'),
}


class Purchase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='purchase')
    shop = models.ForeignKey(to=Shop, on_delete=models.DO_NOTHING, related_name='purchase')
    dateTime = models.DateTimeField()
    endTime = models.DateTimeField()
    status = models.CharField(choices=PCH_STATUS, max_length=2)
