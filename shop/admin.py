from django.contrib import admin

# Register your models here.
from shop import models

admin.site.register(models.Shop)
admin.site.register(models.SecondaryCategory)
admin.site.register(models.PrimaryCategory)
admin.site.register(models.Service)
admin.site.register(models.Schedule)

