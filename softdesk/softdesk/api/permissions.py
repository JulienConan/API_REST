from rest_framework import permissions


class ProjectPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            print('kdjshfksjd')
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


class UserPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if view.action =='list':
            return request.user in obj.contributors.all()
        elif view.action =='create':
            return request.user == obj.author
        elif view.action == 'destroy':
            return request.user == obj.author
        else:
            return False


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