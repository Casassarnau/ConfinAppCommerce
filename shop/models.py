from django.db import models


class Shop(models.Model):
    CIF = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=30)
    meanTime = models.FloatField(null=True, blank=True)

    latitude = models.DecimalField(decimal_places=7, max_digits=11, null=True, blank=True)
    longitude = models.DecimalField(decimal_places=7, max_digits=11, null=True, blank=True)

