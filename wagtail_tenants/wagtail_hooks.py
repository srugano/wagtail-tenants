from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _
from wagtail import hooks
from wagtail.admin.menu import MenuItem

from wagtail_tenants.utils import get_allowed_features, get_tenant_aware_apps

from .admin import TenantAdminGroup
from .panels import TenantPanel
from .views import LinkAdminView


@hooks.register("register_admin_viewset")
def register_tenant_admin_viewset():
    """
    Registers the SnippetViewSetGroup for Client, Domain, and Backup models.
    """
    return TenantAdminGroup()


@hooks.register("register_admin_menu_item")
def register_link_admin_menu_item():
    """
    Registers the 'Link Admin' menu item.
    """
    return MenuItem(
        label=_("Link Admin"),
        url=reverse("wagtail-tenants__admin_link"),
        name="link-admin",
        icon_name="group",
        order=602,
    )


@hooks.register("register_admin_urls")
def tenant_user_create_url():
    """
    Registers the URL for the 'Link Admin' view.
    """
    return [
        path(
            "wagtail-tenants/admin/link/",
            LinkAdminView.as_view(),
            name="wagtail-tenants__admin_link",
        ),
    ]


@hooks.register("construct_homepage_panels")
def add_wagtail_tenants_panels(request, panels):
    if request.tenant.schema_name != "public":
        panels.append(TenantPanel())


@hooks.register("construct_main_menu")
def customize_menu_for_tenant(request, menu_items):
    current_tenant = request.tenant
    # Get the allowed feature menu names for the current tenant
    allowed_features = get_allowed_features(current_tenant)
    # Get the tenant-aware app names
    tenant_aware_apps = get_tenant_aware_apps(current_tenant)
    # Filter the menu items based on the allowed features and tenant-aware apps
    menu_items[:] = [
        item
        for item in menu_items
        if (item.name in allowed_features and item.name in tenant_aware_apps)
        or item.name not in tenant_aware_apps
    ]
