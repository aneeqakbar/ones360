from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Country, Province, City, Role, User

# Register your models here.

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
    empty_value_display = '-empty-'

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "get_image", "email", "mobile_number", "country")
    empty_value_display = '-empty-'

    def get_image(self, ins):
        return mark_safe(f"<img src='{ins.profile_image.url}' height='50px' style='box-shadow: 1px 1px 5px 1px rgba(0,0,0,.3);' />")
    get_image.short_description = "Profile Pic"


class CityInline(admin.StackedInline):
    model = City
    extra = 0
    min_num = None
    max_num = None

class ProvinceInline(admin.StackedInline):
    model = Province
    extra = 0
    min_num = None
    max_num = None

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "get_image", "country_code", "currency_code", "phone_code", "phone_format", "get_date_of_creation")
    empty_value_display = '-empty-'
    inlines = [ProvinceInline, CityInline]

    def get_image(self, ins):
        return mark_safe(f"<img src='{ins.image.url}' height='50px' style='box-shadow: 1px 1px 5px 1px rgba(0,0,0,.3);' />")
    get_image.short_description = "Flag"

    def get_date_of_creation(self, ins):
        return ins.date_of_creation.date()
    get_image.short_description = "Date of creation"