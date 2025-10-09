from django.urls import path
from instagrapi.mixins import signup
from . import views


urlpatterns = [
    path('',views.home, name='home'),   # ← صفحه اصلی
    path('about/', views.about, name='about'),  # ← درباره ما
    path('login/',views.login_user, name='login'),
    path('logout/',views.logout_user, name='logout'),
    path('signup/',views.signup_user, name='signup'),
    path('product/<int:pk>',views.product, name='product'),
    path('category/<str:cat>',views.category, name='category'),
    path('category/',views.category_summery, name='category_summery'),
    path('update_user/',views.update_user, name='update_user'),
    path('update_password/',views.update_password, name='update_password'),
    path('update_info',views.update_info, name='update_info'),
    path('search/',views.search, name='search'),
    path('orders/',views.user_orders, name='orders'),
    path('order_details/<int:pk>',views.order_details, name='order_details'),

]
