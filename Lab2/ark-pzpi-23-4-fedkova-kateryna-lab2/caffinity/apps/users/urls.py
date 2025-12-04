from django.urls import path
from rest_framework import routers
from apps.users.views import OrganisationViewSet, RoleViewSet, UserViewSet, RegistrationAPIView, LoginAPIView

router = routers.DefaultRouter()
router.register('organisations', OrganisationViewSet)
router.register('roles', RoleViewSet)
router.register('users', UserViewSet)
urlpatterns = [
    path('auth/register', RegistrationAPIView.as_view()),
    path('auth/login', LoginAPIView.as_view()),
    *router.urls
]
