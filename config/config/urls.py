
from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf import settings
from django.conf.urls.static import static
from rooms import views as room_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("conversations/", include("conversations.urls", namespace="conversations")),
    path("", include("core.urls", namespace="core")),
    path("lists/", include("lists.urls", namespace="lists")),
    path("reservations/", include("reservations.urls", namespace="reservations")),
    path("reviews/", include("reviews.urls", namespace="reviews")),
    path("rooms/", include("rooms.urls", namespace="rooms")),
    path("users/", include("users.urls", namespace="users")),


    # path("users", include("users.urls", namespace="users")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)