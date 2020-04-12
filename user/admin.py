from django.contrib import admin
from django.contrib.admin.forms import AdminPasswordChangeForm

from user.forms import UserChangeForm
from user.models import User


# Admin model
class UserAdmin(admin.ModelAdmin):
    form = UserChangeForm
    change_password_form = AdminPasswordChangeForm

    list_display = ('email', 'name', 'is_shopAdmin', 'is_admin', 'is_client')
    list_filter = ('is_shopAdmin', 'is_admin')

    search_fields = ('email', 'name')
    ordering = ('created_time',)
    date_hierarchy = 'created_time'
    filter_horizontal = ()

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(UserAdmin, self).get_fieldsets(request, obj)


# Adding admin Model to Admin site
admin.site.register(User, UserAdmin)
