from django import forms

from authentication.models import Role
from .models import TailorLegalDocuments, TailorShop
from django.contrib.auth import get_user_model

User = get_user_model()


class CreateShopForm(forms.ModelForm):
    class Meta:
        model = TailorShop
        fields = [
            "owner",
            "name",
            "category",
            "services",
            "interested",
            "address",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = User.objects.filter(role__id=Role.SHOPOWNER).values_list("id","full_name")
        self.fields['owner'].choices = choices

class EditShopForm(forms.ModelForm):
    class Meta:
        model = TailorShop
        fields = [
            "name",
            "description",
            "logo",
            "delivery_location",
            "address",
            "google_address",
            "latitude",
            "longitude",
            "category",
            "services",
            "employees",
            "interested",
            "appointments_per_hour",
            "approval_stage",
            "application_status",
            "city",
            "status",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = User.objects.filter(role__id=Role.EMPLOYEE).values_list("id","full_name")
        self.fields['employees'].choices = choices

class LegalDocumentsForm(forms.ModelForm):
    class Meta:
        model = TailorLegalDocuments
        fields = [
            "id_card_front",
            "id_card_back",
            "commercial_license1",
            "commercial_license2",
            "signature",
        ]