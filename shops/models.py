from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.

User = get_user_model()


SHOP_CATEGORIES = (
    ("M", "Men"),
    ("W", "Women"),
    ("K", "Kids"),
    ("A", "All"),
)

WEEK_DAYS = (
    ("M", "Monday"),
    ("TU", "Tuesday"),
    ("W", "Wednesday"),
    ("TH", "Thursday"),
    ("F", "Friday"),
    ("SA", "Saturday"),
    ("SU", "Sunday"),
)

APPLICATION_STATUS = (
    ("DP", "Documents Pending"),
    ("DS", "Documents Submited"),
    ("UR", "Under Review"),
    ("A", "Approved"),
    ("R", "Rejected"),
)

SHOP_INTERESTS = (
    ("PO", "POS"),
    ("Ad", "Add shop online"),
)

class TailorShop(models.Model):
    owner = models.ForeignKey(User, verbose_name=_("owner"), on_delete=models.CASCADE, related_name="shops")
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), )
    employees = models.ManyToManyField(User, verbose_name=_("employees"), blank=True)
    logo = models.ImageField(_("logo"), upload_to="shops_logos/", null=True)
    city = models.ForeignKey("authentication.City", verbose_name=_("city"), on_delete=models.CASCADE, related_name="shops", null=True)
    address = models.TextField(_("address"))
    services = models.ManyToManyField("shops.ShopService", verbose_name=_("services"), blank=True, related_name="shops")
    interested = models.CharField(_("interested"), max_length=50, choices=SHOP_INTERESTS)
    google_address = models.TextField(_("google_address"))
    latitude = models.CharField(_("latitude"), max_length=100)
    longitude = models.CharField(_("longitude"), max_length=100)
    category = models.CharField(_("category"), max_length=50, choices=SHOP_CATEGORIES)
    status = models.BooleanField(_("status"), default=True)
    appointments_per_hour = models.IntegerField(_("appointments per hour"), default=0)
    approval_stage = models.CharField(_("approval_stage"), max_length=50, choices=APPLICATION_STATUS)
    application_status = models.CharField(_("application_status"), max_length=255)
    delivery_location = models.CharField(_("delivery_location"), max_length=255)
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)


    @property
    def get_edit_url(self):
        try:
            return reverse("shops:EditShopView", kwargs={"shop_id": self.id})
        except:
            return ''

    @property
    def get_banner_url(self):
        try:
            return reverse("shops:EditBannerView", kwargs={"shop_id": self.id})
        except:
            return ''

    @property
    def get_logo_url(self):
        try:
            return self.logo.url
        except:
            return ''

class TailorFabric(models.Model):
    shop = models.ForeignKey(TailorShop, verbose_name=_("shop"), on_delete=models.CASCADE, related_name="fabrics")
    name = models.CharField(max_length=255)
    article_number = models.CharField(max_length=255)
    shades = models.CharField(max_length=255)
    ref_no = models.CharField(max_length=255)
    made_in = models.ForeignKey("authentication.Country", verbose_name=_("country"), on_delete=models.CASCADE, null=True, blank=True)
    price_per_meter = models.IntegerField(_("price_per_meter"), default=0)
    image = models.ImageField(_("logo"), upload_to="fabrics/", null=True)
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)

class TailorLegalDocuments(models.Model):
    shop = models.ForeignKey(TailorShop, verbose_name=_("shop"), on_delete=models.CASCADE, related_name="legal_documents")
    id_card_front = models.ImageField(_("id_card_front"), upload_to="id_cards/", null=True)
    id_card_back = models.ImageField(_("id_card_back"), upload_to="id_cards/", null=True)
    commercial_license1 = models.ImageField(_("commercial_license"), upload_to="commercial_licenses/", null=True)
    commercial_license2 = models.ImageField(_("commercial_license"), upload_to="commercial_licenses/", null=True)
    signature = models.ImageField(_("signature"), upload_to="signatures/", null=True)

class TailorShopBanner(models.Model):
    shop = models.ForeignKey(TailorShop, verbose_name=_("shop"), on_delete=models.CASCADE, related_name="banners")
    image = models.ImageField(_("image"), upload_to="banners/", null=True)

class TailorTiming(models.Model):
    day = models.CharField(_("day"), max_length=50, choices=WEEK_DAYS)
    start_time = models.TimeField(_("start_time"), auto_now=False, auto_now_add=False)
    end_time = models.TimeField(_("end_time"), auto_now=False, auto_now_add=False)

class TailorAppointmentLocation(models.Model):
    shop = models.ForeignKey(TailorShop, verbose_name=_("shop"), on_delete=models.CASCADE, related_name="appointment_locations")
    location = models.CharField(_("location"), max_length=50)

# class TailorDesignations(models.Model):
#     shop = models.ForeignKey(TailorShop, verbose_name=_("shop"), on_delete=models.CASCADE, related_name="appointment_locations")
#     # name = 


class ShopService(models.Model):
    ALTERATION = 1
    NEW_STITCHING = 2
    FABRIC = 3
    READYMADE = 4
    CHOICES = (
        (ALTERATION, 'Alteration'),
        (NEW_STITCHING, 'New Stitching'),
        (FABRIC, 'Fabric'),
        (READYMADE, 'Ready Made'),
    )

    id = models.PositiveSmallIntegerField(choices=CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()

class ShopDevice(models.Model):
    DEVICE_TYPES = (
        ("M", "Mobile"),
        ("T", "Tablet")
    )
    OS_TYPES = (
        ("A", "Android"),
        ("IP", "Iphone")
    )
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    device_id = models.CharField(_("device_id"), max_length=500, null=False)
    device_type = models.CharField(_("device_type"), max_length=50, choices=DEVICE_TYPES, default="M")
    manufaturer = models.CharField(_("manufaturer"), max_length=255, null=True)
    device_name = models.CharField(_("device_name"), max_length=255, null=False)
    Device_Model = models.CharField(_("Device_Model"), max_length=255, null=False)
    OS_Type = models.CharField(_("OS_Type"), max_length=50, choices=OS_TYPES, default="A")
    OS_ID = models.CharField(_("OS_ID"), max_length=255, null=True)