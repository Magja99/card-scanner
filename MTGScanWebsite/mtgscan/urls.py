from django.urls import path
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("card/<int:card_id>", views.card_by_id, name="card_by_id"),
    path("accounts/register/", views.register, name="register"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/login/profile/", views.profile, name="profile"),
    path(
        "accounts/login/profile/show_collection",
        views.show_collection,
        name="show_collection",
    ),
    path("accounts/login/profile/add_cards", views.add_cards, name="add_cards"),
    # path('', views.add_cards, name="add_cards")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
