from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

from django.urls import path

from ..viewsets.ReviewViewSet import ReviewViewSet
from ..viewsets.ProposalViewSet import ProposalViewSet
from ..viewsets.ListingViewSet import ListingViewSet, activate_listing
from ..viewsets.JWTViewSets import RegistrationView, BlacklistView
from ..viewsets.UserViewSets import (
    UpdateUserViewSet,
    UserProfileView,
    user_exists,
    email_exists,
)
from ..viewsets.ApartmentViewSets import (
    ApartmentViewSet,
    like_apartment,
    ApartmentPhotoViewSet,
)

router = DefaultRouter()
router.register(r"apartments", viewset=ApartmentViewSet)
router.register(r"listings", viewset=ListingViewSet)
router.register(r"proposals", viewset=ProposalViewSet)
router.register(r"reviews", viewset=ReviewViewSet)

urlpatterns = [
    path("auth/register/", RegistrationView.as_view(), name="register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/logout/", BlacklistView.as_view(), name="logout"),
    path("me/", UserProfileView, name="profile"),
    path("user_exists/", user_exists, name="user_exists"),
    path("email_exists/", email_exists, name="email_exists"),
    path("apartments/like/<int:apt_id>/", like_apartment, name="like_apartment"),
    path(
        "apartments/<int:apt_id>/photos/",
        ApartmentPhotoViewSet.as_view({"post": "create", "get": "list"}),
        name="apartment_photos_create",
    ),
    path(
        "apartments/<int:apt_id>/photos/<int:photo_id>",
        ApartmentPhotoViewSet.as_view({"delete": "destroy"}),
        name="apartment_photo_delete",
    ),
    path(
        "listings/activate/<int:listing_id>/", activate_listing, name="activate_listing"
    ),
    path(
        "users/<int:user_id>/",
        UpdateUserViewSet.as_view({"patch": "partial_update", "put": "update"}),
        name="update_user",
    ),
] + router.urls
