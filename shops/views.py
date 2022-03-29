from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import get_user_model
# from authentication.forms import UserRegisterForm
from shops.forms import CreateShopForm, EditShopForm, LegalDocumentsForm

from shops.models import TailorShop, TailorShopBanner, TailorAppointmentLocation

# Create your views here.

User = get_user_model()

class DashboardView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("authentication:login")
        context = {
            "dashboard": "Tailor Dashboard",
            "page": "Main",
        }
        return render(request, "dashboard/tailor_home.html", context)

class ManageShopView(View):
    def get(self, request):
        shops = TailorShop.objects.filter(status = True)

        create_shop_form = CreateShopForm()
        legal_documents_form = LegalDocumentsForm()
        context = {
            "legal_documents_form": legal_documents_form,
            "create_shop_form": create_shop_form,
            "type": "tailor",
            "data": shops
        }
        return render(request, "dashboard/manage_shop.html", context)

    def post(self, request):
        create_shop_form = CreateShopForm(request.POST, request.FILES)
        shops = TailorShop.objects.filter(status = False)
        
        action = request.POST.get("action", None)
        shop_id = request.POST.get("shop_id", None)

        if action == "delete":
            shop = get_object_or_404(TailorShop, id = shop_id)
            shop.status = False
            shop.save()
            messages.success(request, "Shop Deleted Successfully")

        elif action == "create":
            if create_shop_form.is_valid():
                shop = create_shop_form.save()
                legal_documents_form = LegalDocumentsForm(request.POST, request.FILES, instance=shop.legal_documents.all().first())
                if legal_documents_form.is_valid():
                    docs = legal_documents_form.save(commit=False)
                    docs.shop = shop
                    docs.save()

                shopBanners = request.FILES.getlist('shop-banner', [])
                appointmentLocations = request.POST.getlist('appointment-location', [])
                for banner in shopBanners:
                    TailorShopBanner.objects.create(
                        shop=shop,
                        image=banner
                    )
                for location in appointmentLocations:
                    TailorAppointmentLocation.objects.create(
                        shop=shop,
                        location=location
                    )
                messages.success(request, "Created Shop Successfully")

        context = {
            "create_shop_form": create_shop_form,
            "data": shops
        }
        return render(request, "dashboard/manage_shop.html", context)


class EditShopView(View):
    def get(self, request, shop_id):
        shop_instance = get_object_or_404(TailorShop, id = shop_id)
        edit_shop_form = EditShopForm(instance=shop_instance)
        legal_documents_form = LegalDocumentsForm(instance=shop_instance.legal_documents.all().first())
        context = {
            "form": edit_shop_form,
            "legal_documents_form": legal_documents_form,
            "shop_instance": shop_instance,
        }
        return render(request, "dashboard/edit_shop.html", context)

    def post(self, request, shop_id):
        shop_instance = get_object_or_404(TailorShop, id = shop_id)
        legal_documents_form = LegalDocumentsForm(instance=shop_instance.legal_documents.all().first())
        edit_shop_form = EditShopForm(request.POST, request.FILES, instance=shop_instance)
        if edit_shop_form.is_valid():
            edit_shop_form.save()
            # if legal_documents_form.is_valid():
            #     legal_documents_form.save()

            # shopBanners = request.FILES.getlist('shop-banner', [])
            # appointmentLocations = request.POST.getlist('appointment-location', [])
            # if shopBanners:
            #     TailorShopBanner.objects.filter(shop=shop_instance).delete()
            #     for banner in shopBanners:
            #         TailorShopBanner.objects.create(
            #             shop=shop_instance,
            #             image=banner
            #         )
            # if appointmentLocations:
            #     TailorAppointmentLocation.objects.filter(shop=shop_instance).delete()
            #     for location in appointmentLocations:
            #         TailorAppointmentLocation.objects.create(
            #             shop=shop_instance,
            #             location=location
            #         )
            messages.success(request, "Updated Store Successfully")
        context = {
            "form": edit_shop_form,
            "shop_instance": shop_instance,
            "legal_documents_form": legal_documents_form,
        }
        return render(request, "dashboard/edit_shop.html", context)


class EditBannerView(View):

    def post(self, request, shop_id):
        shop_instance = get_object_or_404(TailorShop, id = shop_id)
        legal_documents_form = LegalDocumentsForm(instance=shop_instance.legal_documents.all().first())
        edit_shop_form = EditShopForm(instance=shop_instance)
        # if legal_documents_form.is_valid():
        #     legal_documents_form.save()

        shopBanners = request.FILES.getlist('shop-banner', [])
        appointmentLocations = request.POST.getlist('appointment-location', [])
        if shopBanners:
            TailorShopBanner.objects.filter(shop=shop_instance).delete()
            for banner in shopBanners:
                TailorShopBanner.objects.create(
                    shop=shop_instance,
                    image=banner
                )
        if appointmentLocations:
            TailorAppointmentLocation.objects.filter(shop=shop_instance).delete()
            for location in appointmentLocations:
                TailorAppointmentLocation.objects.create(
                    shop=shop_instance,
                    location=location
                )
        # messages.success(request, "Updated Store Successfully")
        context = {
            "form": edit_shop_form,
            "shop_instance": shop_instance,
            "legal_documents_form": legal_documents_form,
        }
        return render(request, "dashboard/edit_shop.html", context)

