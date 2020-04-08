from django.db import models

from user.models import User

SCH_DAYS = [
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
]


class Category(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    class Meta:
        abstract = True


class PrimaryCategory(Category):

    def get_secondaries(self):
        return self.secondary


class SecondaryCategory(Category):
    primary = models.ForeignKey(to=PrimaryCategory, related_name='secondary', on_delete=models.DO_NOTHING)


class Service(Category):
    pass


class Shop(models.Model):
    CIF = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=30)
    meanTime = models.FloatField(null=True, blank=True)

    latitude = models.DecimalField(decimal_places=7, max_digits=11, null=True, blank=True)
    longitude = models.DecimalField(decimal_places=7, max_digits=11, null=True, blank=True)

    admins = models.ManyToManyField(User, related_name='shop')
    secondaryCategories = models.ManyToManyField(to=SecondaryCategory)
    services = models.ManyToManyField(to=Service)


class Schedule(models.Model):
    shop = models.ForeignKey(to=Shop, related_name='schedule', on_delete=models.CASCADE)
    day = models.IntegerField(choices=SCH_DAYS)
    startHour = models.TimeField()
    endHour = models.TimeField()

    class Meta:
        unique_together = (("day", "startHour", 'shop'),)