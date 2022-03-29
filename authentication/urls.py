from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from . import views
from django.contrib.auth import views as auth_views

app_name = "authentication"

urlpatterns = [
    path('', views.HomeView.as_view(), name='HomeView'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', views.UserRegisterView.as_view(), name='UserRegisterView'),
    path('profile/', views.ProfileView.as_view(), name='ProfileView'),
    path('login/', views.LoginView.as_view(), name='LoginView'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('tailor_register/', views.TailorRegisterView.as_view(), name='TailorRegisterView'),
    path('activate/<str:uid>/<str:token>/', views.UserActivateView.as_view(), name='UserActivateView'),
    path('tailor_login/', views.TailorLoginView.as_view(), name='TailorLoginView'),

    path('manage-shop-owner/', views.ManageShopOwnerView.as_view(), name='ManageShopOwnerView'),
    path('manage-cloth-shop-owner/', views.ManageClothOwnerView.as_view(), name='ManageClothOwnerView'),
    path('manage-customer/', views.ManageCustomerView.as_view(), name='ManageCustomerView'),
    path('manage-employee/', views.ManageEmployeeView.as_view(), name='ManageEmployeeView'),
    path('manage-staff/', views.ManageStaffView.as_view(), name='ManageStaffView'),
    path('update-user/<int:user_id>/', views.UpdateUserView.as_view(), name='UpdateUserView'),
    path('manage-user/', views.ManageUserView.as_view(), name='ManageUserView'),
]