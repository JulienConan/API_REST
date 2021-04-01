from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .models import Projects, Issues, Comments


class ProjectPermissions(permissions.BasePermission):
    """ Permissions for Project """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return request.user in obj.contributors.all()
        elif request.method in ['PUT', 'DELETE']:
            return request.user == obj.author
        else:
            return False

class UserPermissions(permissions.BasePermission):
    """Permissions for action on project's collaborators """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return request.user in obj.contributors.all()
        elif request.method in ['POST', 'DELETE']:
            return request.user == obj.author
        else:
            return False


class IssueCommentPermissions(permissions.BasePermission):
    """ Permissions for Issue and Comment """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'POST']:
            return request.user in obj.contributors.all()
        elif request.method in ['PUT', 'DELETE']:
            return request.user == obj.author
        else:
            return False
