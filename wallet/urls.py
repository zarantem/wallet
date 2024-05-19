"""
URL configuration for wallet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from views import CreateWalletView, ViewWalletView, TransferWalletView, DepositWalletView


router = DefaultRouter()


router.register(r'api/v1/create/wallet/', CreateWalletView.as_view(), basename='create-wallet')
router.register(r'api/v1/view/wallet/<str:key_wallet>/', ViewWalletView.as_view(), basename='view-wallet')
router.register(r'api/v1/transfer/wallet/', TransferWalletView.as_view(), basename='transfer-wallet')
router.register(r'api/v1/deposit/wallet/<str:key_wallet>/', DepositWalletView.as_view(), basename='deposit-wallet')