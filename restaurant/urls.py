from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    ReviewCreateView, ReviewListView, ReviewDeleteView,
    DishListView, DishDetailView, DishCreateView, DishUpdateView, DishDeleteView,
    OrderListView, OrderCreateView, OrderDeleteView,
    UserRegisterView, UserLoginView, UserLogoutView,
)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    path('dish', DishListView.as_view(), name='dish_list'),
    path('dish/<int:pk>/', DishDetailView.as_view(), name='dish_detail'),
    path('dish/create/', DishCreateView.as_view(), name='dish_create'),
    path('dish/update/<int:pk>/', DishUpdateView.as_view(), name='dish_update'),
    path('dish/delete/<int:pk>/', DishDeleteView.as_view(), name='dish_delete'),

    path('orders/', OrderListView.as_view(), name='order_list'),
    path('order/create/<int:pk>/', OrderCreateView.as_view(), name='order_create'),
    path('order/delete/<int:pk>/', OrderDeleteView.as_view(), name='order_delete'),

    path('reviews/', ReviewListView.as_view(), name='review_list'),
    path('review/create/<int:pk>/', ReviewCreateView.as_view(), name='review_create'),
    path('review/delete/<int:pk>/', ReviewDeleteView.as_view(), name='review_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
