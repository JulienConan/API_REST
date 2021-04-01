from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .models import Projects, Issues, Comments


class ProjectPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if 'pk' not in view.kwargs:
            return True
        else:
            project = get_object_or_404(Projects, pk=view.kwargs['pk'])
            if request.method == 'GET':
                print('get')
                return request.user in project.contributors.all()
            elif request.method in ['PUT', 'DELETE']:
                return request.user == project.author


class UserPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        project = get_object_or_404(Projects, pk=view.kwargs['projects_pk'])

        if request.method == 'GET':
            return request.user in project.contributors.all()
        if request.method in ['POST', 'DELETE']:
            return request.user == project.author



class IssuePermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if view.action =='list':
            return True
        elif view.action == 'retrieve':
            return True
        elif view.action =='create':
            return True
        elif view.action in ['update', 'partial_update']:
            return obj.author == request.user
        elif view.action == 'destroy':
            return obj.author == request.user
        else:
            return False


class CommentPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if view.action =='list':
            return True
        elif view.action == 'retrieve':
            return True
        elif view.action =='create':
            return True
        elif view.action in ['update', 'partial_update']:
            return obj.author == request.user
        elif view.action == 'destroy':
            return obj.author == request.user
        else:
            return False