from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.models import User  # 👈 اینو اضافه کن

# 👇 این قسمت رو اضافه کن (بالای urlpatterns)
if not User.objects.filter(username="Amir").exists():
    User.objects.create_superuser("Amir", "amirhoseinmahm2002@gmail.com", "A09020039798a")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('cart/', include('cart.urls')),
    path('payment/', include('payment.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
