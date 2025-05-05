from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import CartItemViewSet, CartGetView, PlaceOrderView

app_name = 'cart'


urlpatterns = [
    path('get_user_cart/', CartGetView.as_view()),
    path('place_order/', PlaceOrderView.as_view()),
]

router = SimpleRouter()
router.register(r'cart-items', CartItemViewSet, basename='cart-items')
urlpatterns += router.urls