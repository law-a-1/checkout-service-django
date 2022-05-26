from django.urls import include, path
from .views import CheckoutViewSet, CartViewSet

urlpatterns = [
    path('', CheckoutViewSet.as_view()),
    path('cart/', CartViewSet.as_view()),
]