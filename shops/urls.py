from django.urls import path
from . import views

app_name = "shops"

urlpatterns = [
    path("dashboard/", views.DashboardView.as_view(), name="DashboardView"),
    path("manage-shop/", views.ManageShopView.as_view(), name="ManageShopView"),
    path("edit-shop/<int:shop_id>/", views.EditShopView.as_view(), name="EditShopView"),
    path("edit-shop-banners/<int:shop_id>/", views.EditBannerView.as_view(), name="EditBannerView"),
]