from django.contrib import admin

from purchase import models

# adds purchases to admin view
admin.site.register(models.Purchase)
