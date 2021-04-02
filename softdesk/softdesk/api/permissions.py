from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .models import Projects, Issues, Comments


class ProjectPermissions(permissions.BasePermission):
    """ Permissions for Project """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return request.user in obj.contributors.all()
        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user == obj.author
        else:
            return False


class UserPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        project = get_object_or_404(Projects, pk=view.kwargs['projects_pk'])

        if request.method == 'GET':
            return request.user in project.contributors.all()
        if request.method in ['POST', 'DELETE']:
            return request.user == project.author


class IssueCommentPermissions(permissions.BasePermission):
    """ Permissions for Issue and Comment """

    def has_permission(self, request, view):
        if request.method in ['GET', 'POST', 'DELETE', 'PUT', 'PATCH']:
            print(request.user.pk)
            return request.user in Projects.objects.get(pk=view.kwargs['projects_pk']).contributors.all()

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            print('kjhsqgheikuazjeh')
            return request.user == obj.author
        else:
            return True

