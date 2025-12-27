from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django_tenants.utils import tenant_context
from wagtail.admin import messages
from wagtail.admin.views import account
from wagtail.admin.views.generic.base import WagtailAdminTemplateMixin
from wagtail.admin.views.generic.forms import FormView

from wagtail_tenants.backends import UserModel
from wagtail_tenants.forms import TenantAdminUserForm
from wagtail_tenants.utils import check_tenant_for_user


class TenantLoginView(account.LoginView):
    def get(self, *args, **kwargs):
        if (
            check_tenant_for_user(self.request.user, self.request.tenant)
            and self.request.user.is_authenticated
            and self.request.user.has_perm("wagtailadmin.access_admin")
        ):
            return redirect(self.get_success_url())

        return super().get(*args, **kwargs)


class LinkAdminView(WagtailAdminTemplateMixin, FormView):
    """
    A view to link an existing superuser to a specific tenant.
    """

    form_class = TenantAdminUserForm
    template_name = "wagtail_tenants/admin/link.html"
    page_title = _("Link superuser to tenant")
    header_icon = "user"

    def get_success_url(self):
        return reverse("wagtail-tenants__admin_link")

    def form_valid(self, form):
        superuser = form.cleaned_data["superuser"]
        tenant = form.cleaned_data["tenant"]
        with tenant_context(tenant):
            created = False
            try:
                # Check if the user already exists in the tenant's schema
                UserModel.objects.get(username=superuser.username)
            except UserModel.DoesNotExist:
                # If not, create them
                tenant_admin = UserModel(
                    username=superuser.username,
                    email=superuser.email,
                    password=superuser.password,
                    is_staff=True,
                    is_superuser=True,
                )
                tenant_admin.save()
                created = True

            if created:
                messages.success(
                    self.request,
                    _("Admin '{0}' linked to tenant '{1}'.").format(
                        superuser.username, tenant.name
                    ),
                )
            else:
                messages.warning(
                    self.request,
                    _("Admin '{0}' already exists for tenant '{1}'.").format(
                        superuser.username, tenant.name
                    ),
                )
        return super().form_valid(form)
