from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site

from shops.forms import CreateShopForm
from .tokens import account_activation_token
from django.core.mail import send_mail

from authentication.mixins import RedirectToPanelMixin
from authentication.models import Role
from .forms import InitialShopForm, MobileAuthenticationForm, TailorRegisterForm, UserRegisterForm, UserUpdateForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q

# Create your views here.

User = get_user_model()

class HomeView(RedirectToPanelMixin, View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("authentication:LoginView")


class LoginView(View):
    def get(self, request):
        mobile_form = MobileAuthenticationForm()
        email_form = AuthenticationForm()
        context = {
            "mobile_form": mobile_form,
            "email_form": email_form,
        }
        return render(request, 'dashboard/login.html', context)

    def  post(self, request):
        mobile_form = MobileAuthenticationForm(data=request.POST)
        email_form = AuthenticationForm(data=request.POST)
        print(email_form.is_valid())
        if email_form.is_valid():
            user = email_form.get_user()
            login(request, user)
            return redirect('authentication:HomeView')
        elif mobile_form.is_valid():
            user = mobile_form.get_user()
            login(request, user)
            return redirect('authentication:HomeView')
        context = {
            "mobile_form": mobile_form,
            "email_form": email_form,
        }
        return render(request, 'dashboard/login.html', context)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("authentication:HomeView")

class UserRegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'dashboard/register.html', {'form': form})

    def  post(self, request):
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('authentication:login')
        return render(request, 'dashboard/register.html', {'form': form})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserUpdateForm(instance=request.user)

        context = {
            'form': form,
        }

        return render(request, 'dashboard/profile_edit.html', context)

    def post(self, request):
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)

        print(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('authentication:ProfileView')
        context = {
            'form': form,
        }
        return render(request, 'dashboard/profile_edit.html', context)



class ManageShopOwnerView(View):
    def get(self, request):
        shop_type = request.GET.get("type", None)
        users = User.objects.filter(role__id = Role.SHOPOWNER, is_active = True)
        title =  "Manage Shop Owners"

        if shop_type == "TS":
            users = users.annotate(shop_count=Count('shops')).filter(shop_count__gte = 1)
            title =  "Manage Tailor Shop Owners"
        elif shop_type == "CS":
            users = users.annotate(shop_count=Count('cloth_shops')).filter(shop_count__gte = 1)
            title =  "Manage Cloth Shop Owners"
        print(shop_type == "CS")
        print(shop_type)

        user_creation_form = UserRegisterForm()
        context = {
            "user_creation_form": user_creation_form,
            "title": title,
            "shop_owner": True,
            "data": users
        }
        return render(request, "dashboard/manage_users.html", context)


class ManageClothOwnerView(View):
    def get(self, request):
        users = User.objects.filter(role__id = Role.SHOPOWNER, is_active = True)
        user_creation_form = UserRegisterForm()
        context = {
            "user_creation_form": user_creation_form,
            "title": "Manage Tailor",
            "group": "Tailor",
            "data": users
        }
        return render(request, "dashboard/manage_users.html", context)


class ManageCustomerView(View):
    def get(self, request):
        users = User.objects.filter(role__id = Role.CUSTOMER, is_active = True)
        user_creation_form = UserRegisterForm()
        context = {
            "user_creation_form": user_creation_form,
            "title": "Manage Customer",
            "group": "Customer",
            "data": users
        }
        return render(request, "dashboard/manage_users.html", context)


class ManageStaffView(View):
    def get(self, request):
        users = User.objects.filter(
            Q(role__id = Role.ADMIN) |
            Q(role__id = Role.Staff_1S360) &
            Q(is_active = True)
        )
        user_creation_form = UserRegisterForm()
        context = {
            "user_creation_form": user_creation_form,
            "title": "Manage Employee",
            "group": "Employee",
            "data": users
        }
        return render(request, "dashboard/manage_users.html", context)


class ManageEmployeeView(View):
    def get(self, request):
        users = User.objects.filter(role__id = Role.EMPLOYEE, is_active = True)
        user_creation_form = UserRegisterForm()
        context = {
            "user_creation_form": user_creation_form,
            "title": "Manage Employee",
            "group": "Employee",
            "data": users
        }
        return render(request, "dashboard/manage_users.html", context)


class UpdateUserView(View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id = user_id)
        user_update_form = UserUpdateForm(instance=user)
        context = {
            "form": user_update_form,
            "title": f"Editing User '{user.full_name}'",
            "form_url": reverse("authentication:ManageUserView"),
            "extra_from": f"<input type='hidden' name='action' value='update'><br/><input type='hidden' name='user_id' value='{user.id}'>",
        }
        return render(request, "dashboard/render_form.html", context)

class ManageUserView(View):

    def post(self, request):
        action = request.POST.get("action", None)
        user_id = request.POST.get("user_id", None)

        if action == "create":
            form = UserRegisterForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "User created successfully")

        elif action == "update":
            user = get_object_or_404(User, id = user_id)
            form = UserUpdateForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "User updated successfully")

        elif action == "delete":
            user = get_object_or_404(User, id = user_id)
            user.is_active = False
            user.save()
            messages.success(request, "User disabled successfully")

        elif form.is_valid():
            user = form.save()
            messages.success(request, "User Created Successfully")

        previous_url = request.META.get('HTTP_REFERER')

        if previous_url:
            return redirect(previous_url)
        return redirect("shops:ManageShopOwnerView")



class TailorLoginView(View):
    def get(self, request):
        mobile_form = MobileAuthenticationForm()
        email_form = AuthenticationForm()
        context = {
            "mobile_form": mobile_form,
            "email_form": email_form,
        }
        return render(request, 'dashboard/login.html', context)

    def  post(self, request):
        mobile_form = MobileAuthenticationForm(data=request.POST)
        email_form = AuthenticationForm(data=request.POST)
        print(email_form.is_valid())
        if email_form.is_valid():
            user = email_form.get_user()
            login(request, user)
            return redirect('authentication:HomeView')
        elif mobile_form.is_valid():
            user = mobile_form.get_user()
            login(request, user)
            return redirect('authentication:HomeView')
        context = {
            "mobile_form": mobile_form,
            "email_form": email_form,
        }
        return render(request, 'dashboard/login.html', context)



class TailorRegisterView(View):
    def get(self, request):
        form = TailorRegisterForm()
        shop_form = InitialShopForm()
        context = {
            'heading': "Sign Up As Tailor",
            'form': form,
            'shop_form': shop_form,
        }
        return render(request, 'dashboard/tailor_register_form.html', context)

    def post(self, request):
        form = TailorRegisterForm(request.POST, request.FILES)
        shop_form = InitialShopForm(request.POST, request.FILES)
        if form.is_valid() and shop_form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            shop = shop_form.save(commit=False)
            shop.owner = user
            shop.save()

            token = account_activation_token.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activation_url = reverse("authentication:UserActivateView", kwargs={'token': token, 'uid': uid})
            print(activation_url)
            # current_site = get_current_site(request)
            # mail_subject = 'Activate your account.'
            # message = render_to_string('email_template.html', {
            #             'user': user,
            #             'domain': current_site.domain,
            #             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #             'token': account_activation_token.make_token(user),
            #         })
            # to_email = form.cleaned_data.get('email')
            # send_mail(mail_subject, message, 'youremail', [to_email])
            messages.success(request, f'Your account has been created! Please check your email for verification.')
            return redirect('authentication:TailorRegisterView')
        context = {
            'heading': "Sign Up As Tailor",
            'form': form,
            'shop_form': shop_form,
        }
        return render(request, 'dashboard/tailor_register_form.html', context)


class UserActivateView(View):
    def get(self, request, uid, token):
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        else:
            return HttpResponse('Activation link is invalid!')