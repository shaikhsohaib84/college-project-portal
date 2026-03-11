from django.shortcuts import redirect
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", lambda request: redirect("login")),  # 👈 THIS LINE ADDED
    path("admin/", admin.site.urls),
    path("projects/", include("projects.urls")),
    path("accounts/", include("accounts.urls")),  # ADD THIS
    path('', include('accounts.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)