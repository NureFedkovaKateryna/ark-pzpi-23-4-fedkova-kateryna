from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Organisation, Role, User


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
    class Meta:
        model = User
        fields = '__all__'
