from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("authentication:login")
        context = {
            "dashboard": "Admin Dashboard",
            "page": "Main",
        }
        return render(request, "dashboard/admin_home.html", context)