from django import forms
from django.forms import ValidationError
from django.contrib.auth import get_user_model, authenticate
from django.utils.text import capfirst
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from authentication.models import Country, Role

User = get_user_model()




class MobileAuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    email/password or mobile_number/password logins.
    """

    mobile_number = forms.CharField(required=True, label=_("Mobile Number"), strip=True)

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "username" field.
        self.username_field = User._meta.get_field("mobile_number")
        username_max_length = self.username_field.max_length or 254
        self.fields["mobile_number"].max_length = username_max_length
        self.fields["mobile_number"].widget.attrs["maxlength"] = username_max_length
        if self.fields["mobile_number"].label is None:
            self.fields["mobile_number"].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get("mobile_number")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, mobile_number=username, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
            params={"username": self.username_field.verbose_name},
        )




class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True)
    phone_code = forms.ChoiceField(choices=[])
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = Country.objects.all().values_list("phone_code","phone_code")
        self.fields['phone_code'].choices = choices

    class Meta:
        model = User
        fields = [
            'full_name',
            'email',
            'phone_code',
            'mobile_number',
            'whatsapp_number',
            'password1',
            'password2',
            'role',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = str(self.cleaned_data["full_name"]).lower().replace(" ", "_")
        user.mobile_number = str(self.cleaned_data["phone_code"]) + str(self.cleaned_data["mobile_number"])
        try:
            user.first_name = str(self.cleaned_data["full_name"]).split(" ")[0]
            user.last_name = str(self.cleaned_data["full_name"]).split(" ")[1]
        except:
            pass
        if commit:
            user.save()
        return user



class UserUpdateForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = [
            'full_name',
            'email',
            'mobile_number',
            'whatsapp_number',
            'date_of_birth',
            'gender',
            'profile_image',
            'about',
            'detail_address',
            'google_address',
            'longitude',
            'latitude',
            'country',
            'city',
        ]




class TailorRegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True)
    phone_code = forms.ChoiceField(choices=[])
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = Country.objects.all().values_list("phone_code","phone_code")
        self.fields['phone_code'].choices = choices

    class Meta:
        model = User
        fields = [
            'full_name',
            'email',
            'phone_code',
            'mobile_number',
            'whatsapp_number',
            'password1',
            'password2',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        role, created = Role.objects.get_or_create(id = Role.SHOPOWNER)
        user.role = role
        user.username = str(self.cleaned_data["full_name"]).lower().replace(" ", "_")
        user.mobile_number = str(self.cleaned_data["phone_code"]) + str(self.cleaned_data["mobile_number"])
        try:
            user.first_name = str(self.cleaned_data["full_name"]).split(" ")[0]
            user.last_name = str(self.cleaned_data["full_name"]).split(" ")[1]
        except:
            pass
        if commit:
            user.save()
        return user

