import uuid

from django.db import models

from shop.models import Shop
from user.models import User

PCH_PENDING = 'P'
PCH_ACCEPTED = 'A'
PCH_EXPIRED = 'E'

PCH_STATUS = [
    (PCH_PENDING, 'Pendent'),
    (PCH_ACCEPTED, 'Acceptat'),
    (PCH_EXPIRED, 'Caducat'),
]
PCH_STR_POS = {
    'P': 0,
    'A': 1,
    'E': 2,
}


class Purchase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='purchase')
    shop = models.ForeignKey(to=Shop, on_delete=models.CASCADE, related_name='purchase')
    dateTime = models.DateTimeField()
    endTime = models.DateTimeField()
    status = models.CharField(choices=PCH_STATUS, max_length=2)

    # gets string from status
    def status_str(self):
        return PCH_STATUS[PCH_STR_POS[self.status]][1]

    def is_pending(self):
        return self.status == PCH_PENDING

    # accept the purchase
    def accept(self):
        self.status = PCH_ACCEPTED

    # expire the purchase
    def expire(self):
        self.status = PCH_EXPIRED
