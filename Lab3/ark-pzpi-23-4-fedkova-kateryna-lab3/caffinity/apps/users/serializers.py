from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Organisation, Role, User
from .utils import generate_temp_password


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, max_length=100)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    organisation_title = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'organisation_title']

    def create(self, validated_data):
        validated_data['role'] = 'Owner'
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'token']

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError('An email address is required to log in.')

        if password is None:
            raise serializers.ValidationError('A password is required to log in.')

        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError('A user was not found.')

        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated.')

        return {
            'token': user.token
        }


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "username", "is_active", "role", "organisation", "password"]
        read_only_fields = []

    def get_fields(self):
        fields = super().get_fields()
        user = self.context["request"].user
        if not user.is_authenticated:
            return fields
        if not (user.role.title in ("Admin", "Owner")):
            fields["role"].read_only = True
            fields["organization"].read_only = True
            fields["is_active"].read_only = True
        return fields

    def update(self, instance, validated_data):
        new_password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if new_password:
            instance.set_password(new_password)
        instance.save()
        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    temp_password = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "username", "temp_password", "is_active", "role", "organisation"]

    def create(self, validated_data):
        temp_password = generate_temp_password()
        user = User(**validated_data)
        user.set_password(temp_password)
        user.save()
        user.temp_password = temp_password
        return user
