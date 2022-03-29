from django.db import models
from django.contrib.auth.models import User, AbstractUser
from PIL import Image
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

GENDER_CHOICES = (
    ("F", "Female"),
    ("M", "Male"),
    ("O", "Other"),
)

class Role(models.Model):
  EMPLOYEE = 1
  CUSTOMER = 2
  SHOPOWNER = 3
  ADMIN = 4
  Staff_1S360 = 5
  ROLE_CHOICES = (
    (EMPLOYEE, 'Shop_Employee'),
    (CUSTOMER, 'Customer'),
    (SHOPOWNER, 'Shop_Owner'),
    (Staff_1S360, 'Staff_1S360'),
    (ADMIN, 'Super_Admin'),
  )

  id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

  def __str__(self):
    return self.get_id_display()

class User(AbstractUser):

    full_name = models.CharField(_("full_name"), max_length=255, null=True)

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=False,
        help_text=_(
            "150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        null=True,
        blank=True
    )

    email = models.EmailField(
        _("email"),
        max_length=255,
        unique=True,
        null=False,
        help_text=_(
            "Enter your email address here."
        ),
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )

    mobile_number = models.CharField(
        _("mobile_number"),
        max_length=255,
        unique=True,
        null=False,
        help_text=_(
            "Enter your mobile number here."
        ),
        error_messages={
            "unique": _("A user with that mobile number already exists."),
        },
    )

    whatsapp_number = models.CharField(_("whatsapp_number"), max_length=255, blank=True)
    date_of_birth = models.DateTimeField(_("date_of_birth"), auto_now=False, auto_now_add=False, null=True, blank=True)
    gender = models.CharField(_("gender"), max_length=50, choices=GENDER_CHOICES)
    profile_image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics/', null=True)
    about = models.TextField(blank=True)
    country = models.ForeignKey("authentication.Country", verbose_name=_("country"), on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey("authentication.City", verbose_name=_("city"), on_delete=models.CASCADE, null=True, blank=True)
    detail_address = models.TextField(_("detail_address"), blank=True)
    google_address = models.TextField(_("google_address"), blank=True)
    longitude = models.IntegerField(_("longitude"), default=0)
    latitude = models.IntegerField(_("latitude"), default=0)
    role = models.ForeignKey(Role, verbose_name=_("role"), on_delete=models.CASCADE, related_name="users", null=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "mobile_number"]

    def __str__(self):
        return f'{self.username}'

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

        img = Image.open(self.profile_image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_image.path)

    @property
    def get_image_url(self):
        try:
            return self.profile_image.url
        except:
            return ''

    @property
    def get_name(self):
        try:
            return str(self.username).replace("_", " ")
        except:
            return ''


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
#     image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics/')
#     bio = models.TextField()
#     phone = models.CharField(max_length=255, null=True, blank=True)
#     city = models.ForeignKey("authentication.City", verbose_name=_("city"), on_delete=models.CASCADE, related_name="users", null=True)

#     def __str__(self):
#         return f'{self.user.username} Profile'

#     def save(self, *args, **kwargs):
#         super(Profile, self).save(*args, **kwargs)

#         img = Image.open(self.image.path)

#         if img.height > 300 or img.width > 300:
#             output_size = (300, 300)
#             img.thumbnail(output_size)
#             img.save(self.image.path)

#     @property
#     def get_image_url(self):
#         try:
#             return self.image.url
#         except:
#             return ''

# @receiver(post_save, sender=User)
# def create_profile(sender, created, instance, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


class Country(models.Model):
    name = models.CharField(_("name"), max_length=255)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='country_flags/', null=True)
    country_code = models.CharField(_("country_code"), max_length=50, null=True)
    currency_code = models.CharField(_("currency_code"), max_length=50, null=True)
    phone_code = models.CharField(_("phone_code"), max_length=50, null=True)
    phone_format = models.CharField(_("phone_format"), max_length=50, null=True)
    date_of_creation = models.DateTimeField(_("date_of_creation"), auto_now=False, auto_now_add=False, null=True)
    status = models.BooleanField(_("status"), default=True, null=True)
    
    def __str__(self):
        return f"{self.name}"


    # @property
    # def get_shops(self):
    #     shop_ids = self.cities.all().values_list("shops", flat=True)
    #     return Shop.objects.filter(id__in = shop_ids)

class Province(models.Model):
    country = models.ForeignKey(Country, verbose_name=_("country"), on_delete=models.CASCADE, related_name="provinces")
    name = models.CharField(_("name"), max_length=255)
    date_of_creation = models.DateTimeField(_("date_of_creation"), auto_now=False, auto_now_add=False, null=True)
    status = models.BooleanField(_("status"), default=True)

    def __str__(self):
        return f"{self.country.name} -> {self.name}"

    # @property
    # def get_shops(self):
    #     shop_ids = self.cities.all().values_list("shops", flat=True)
    #     return Shop.objects.filter(id__in = shop_ids)

class City(models.Model):
    country = models.ForeignKey(Country, verbose_name=_("country"), on_delete=models.CASCADE, related_name="cities")
    province = models.ForeignKey(Province, verbose_name=_("province"), on_delete=models.CASCADE, related_name="cities")
    name = models.CharField(_("name"), max_length=255)
    date_of_creation = models.DateTimeField(_("date_of_creation"), auto_now=False, auto_now_add=False, null=True)
    status = models.BooleanField(_("status"), default=True)

    def __str__(self):
        return f"{self.country.name} -> {self.province.name} -> {self.name}"