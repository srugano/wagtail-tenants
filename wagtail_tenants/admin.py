from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from wagtail_tenants.customers.models import Client, ClientBackup, Domain

from .models import User


# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        "username",
        "email",
        "tenant",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                    "tenant",
                )
            },
        ),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "tenant",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


class TenantClientAdmin(SnippetViewSet):
    model = Client
    list_display = ("name", "paid_until", "on_trial", "created_on")
    icon = "user"
    menu_label = _("Clients")


class TenantDomainAdmin(SnippetViewSet):
    model = Domain
    list_display = ("domain", "tenant")
    icon = "redirect"
    menu_label = _("Domains")


class TenantBackupAdmin(SnippetViewSet):
    model = ClientBackup
    list_display = (
        "filename",
        "created_at",
    )
    icon = "redirect"
    menu_label = _("Backups")


class TenantAdminGroup(SnippetViewSetGroup):
    menu_label = _("Tenants")
    icon = "group"
    items = (TenantClientAdmin, TenantDomainAdmin, TenantBackupAdmin)
