from django.contrib import admin
from .models import ClothAppointmentLocation, ClothShopBanner, ClothLegalDocuments, ClothShop, ClothFabric
# Register your models here.

class AppointmentLocationInline(admin.StackedInline):
    model = ClothAppointmentLocation
    extra = 0
    min_num = None
    max_num = None

class BannersInline(admin.StackedInline):
    model = ClothShopBanner
    extra = 0
    min_num = None
    max_num = None

class LegalDocumentsInline(admin.StackedInline):
    model = ClothLegalDocuments
    extra = 0
    min_num = None
    max_num = None

@admin.register(ClothShop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("owner", "name")
    empty_value_display = '-empty-'
    save_as = True
    inlines = [BannersInline, AppointmentLocationInline, LegalDocumentsInline]

@admin.register(ClothFabric)
class FabricAdmin(admin.ModelAdmin):
    list_display = ("name", )
    empty_value_display = '-empty-'

