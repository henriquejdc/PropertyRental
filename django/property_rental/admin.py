from rest_framework.authtoken.models import Token

from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _


class MyAdminSite(admin.AdminSite):
    """Extends the default Admin site."""

    site_title = _("PropertyRental Admin")
    site_header = _("Admin")
    index_title = _("PropertyRental Administration")


property_rental_admin = MyAdminSite(name="property_rental_admin")


class GroupAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]
    filter_horizontal = ("permissions",)


class PermissionAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "content_type", "codename"]
    ordering = ["name"]
    search_fields = ["name", "codename"]


class TokenAdmin(admin.ModelAdmin):
    list_display = ["key", "user", "created"]
    search_fields = ["user__email"]


property_rental_admin.register(Token, TokenAdmin)
property_rental_admin.register(Group, GroupAdmin)
property_rental_admin.register(Permission, PermissionAdmin)
