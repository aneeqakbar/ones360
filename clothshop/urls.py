from django.urls import path
from . import views

app_name = "clothshop"

urlpatterns = [
    path("manage-shop/", views.ManageShopView.as_view(), name="ManageShopView"),
    path("edit-shop/<int:shop_id>/", views.EditShopView.as_view(), name="EditShopView"),
]