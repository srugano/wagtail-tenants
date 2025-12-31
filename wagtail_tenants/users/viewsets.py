from django.contrib.auth import get_user_model
from wagtail.users.views.groups import GroupViewSet as WagtailGroupViewSet
from wagtail.users.views.users import UserViewSet as WagtailUserViewSet

from wagtail_tenants.forms import TenantAwareGroupForm
from wagtail_tenants.users.models import TenantGroup

User = get_user_model()


class GroupViewSet(WagtailGroupViewSet):
    """
    A custom GroupViewSet that uses a tenant-aware form to filter permissions
    based on the current tenant's features.
    """

    model = TenantGroup
    form_class = TenantAwareGroupForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["tenant"] = self.request.tenant
        return kwargs


class UserViewSet(WagtailUserViewSet):
    """
    A custom UserViewSet that filters the user list to only show users
    belonging to the current tenant.
    """

    def get_queryset(self):
        # On the public schema, show all users.
        if self.request.tenant.schema_name == "public":
            return super().get_queryset()
        # On a tenant schema, only show users of that tenant.
        return User.objects.filter(tenant=self.request.tenant)
