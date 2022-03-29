from django.shortcuts import redirect

from authentication.models import Role


class RedirectToPanelMixin():
    """Redirects the user to correct dashboard page"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                if request.user.role.id == Role.ADMIN:
                    return redirect("admin_panel:DashboardView")
                elif request.user.role.id == Role.SHOPOWNER:
                    return redirect("shops:DashboardView")
            except:
                return redirect("admin_panel:DashboardView")
        return super().dispatch(request, *args, **kwargs)
