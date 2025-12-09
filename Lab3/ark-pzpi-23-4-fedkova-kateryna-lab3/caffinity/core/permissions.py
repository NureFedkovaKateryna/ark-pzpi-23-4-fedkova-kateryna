from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.role.title == "Admin"


class IsOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.role.title == "Owner"

    def has_object_permission(self, request, view, obj):
        return request.user.organisation_id == obj.organisation_id


class IsBarista(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.role.title == "Barista"

    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method == "PATCH":
            return user.id == obj.id
        return request.user.organisation_id == obj.organisation_id
