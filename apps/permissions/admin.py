from django.contrib import admin
from .models import Role, Permission

class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "key")
    filter_horizontal = ("permissions",)

    def get_permissions(self, obj):
        return ", ".join([p.key for p in obj.permissions.all()])

    get_permissions.short_description = "Permissions"

admin.site.register(Role, RoleAdmin)
admin.site.register(Permission)
