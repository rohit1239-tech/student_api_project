
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import StudentViewSet, RegisterView


router = DefaultRouter()

router.register(
    r"students",
    StudentViewSet,
    basename="student"
)


urlpatterns = [

    # User registration
    path(
        "auth/register/",
        RegisterView.as_view(),
        name="register"
    ),

    # User login
    path(
        "auth/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair"
    ),

    # Refresh access token
    path(
        "auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),

    # Student CRUD APIs
    path("", include(router.urls)),
]
