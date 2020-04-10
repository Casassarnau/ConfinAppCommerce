from django.contrib import admin

# Register your models here.
from shop import models

# Adding Models to Admin site
admin.site.register(models.Shop)
admin.site.register(models.SecondaryCategory)
admin.site.register(models.PrimaryCategory)
admin.site.register(models.Service)
admin.site.register(models.Schedule)
