from django.contrib import admin

from shops.models import ShopService, TailorAppointmentLocation, TailorFabric, TailorLegalDocuments, TailorShop, TailorShopBanner, ShopDevice

# Register your models here.



class AppointmentLocationInline(admin.StackedInline):
    model = TailorAppointmentLocation
    extra = 0
    min_num = None
    max_num = None

class BannersInline(admin.StackedInline):
    model = TailorShopBanner
    extra = 0
    min_num = None
    max_num = None

class LegalDocumentsInline(admin.StackedInline):
    model = TailorLegalDocuments
    extra = 0
    min_num = None
    max_num = None

@admin.register(TailorShop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("owner", "name")
    empty_value_display = '-empty-'
    save_as = True
    inlines = [BannersInline, AppointmentLocationInline, LegalDocumentsInline]

@admin.register(TailorFabric)
class FabricAdmin(admin.ModelAdmin):
    list_display = ("name", )
    empty_value_display = '-empty-'



@admin.register(ShopService)
class ShopServiceAdmin(admin.ModelAdmin):
    list_display = ("__str__", )
    empty_value_display = '-empty-'



@admin.register(ShopDevice)
class ShopDeviceAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "device_id",
        "device_type",
        "manufaturer",
        "device_name",
        "Device_Model",
        "OS_Type",
        "OS_ID",
    )
    empty_value_display = '-empty-'


