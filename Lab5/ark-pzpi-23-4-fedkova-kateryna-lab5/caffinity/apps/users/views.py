from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from core.permissions import IsOwner, IsAdmin, IsBarista
from .serializers import OrganisationSerializer, RoleSerializer, UserSerializer, RegistrationSerializer, \
    LoginSerializer, UserCreateSerializer
from .models import Organisation, Role, User


class RegistrationAPIView(APIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrganisationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganisationSerializer
    queryset = Organisation.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = IsAdmin
        elif self.action == 'retrieve':
            permission_classes = IsAdmin | IsOwner | IsBarista
        elif self.action in ('create', 'partial_update', 'destroy'):
            permission_classes = IsAdmin | IsOwner
        else:
            permission_classes = IsAuthenticated
        return [permission_classes()]


class RoleViewSet(viewsets.ModelViewSet):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_permissions(self):
        if self.action in ('create', 'partial_update', 'destroy'):
            permission_classes = IsAdmin
        else:
            permission_classes = IsAuthenticated
        return [permission_classes()]


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_queryset(self):
        user = self.request.user
        print(user.role.title)
        if user.role.title == "Admin":
            return User.objects.all()
        return User.objects.filter(organisation_id=user.organisation_id)

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'partial_update'):
            permission_classes = IsAdmin | IsOwner | IsBarista
        elif self.action in ('create', 'destroy'):
            permission_classes = IsOwner | IsAdmin
        else:
            permission_classes = IsAuthenticated
        return [permission_classes()]
