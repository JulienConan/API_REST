from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Projects, Issues, Comments
from .permissions import (
    ProjectPermissions,
    UserPermissions,
    IssueCommentPermissions
)
from .serializers import(
    ProjectsSerializer,
    UsersProjectSerializer,
    IssuesSerializer,
    CommentsSerializer
)


class ProjectsViewSet(viewsets.ViewSet):
    """
        Actions for project
        'GET' = List project
        'POST' = Add project
        'PUT' = Modify project 
        'DELETE' = Delete project
    """

    permission_classes = [IsAuthenticated, ProjectPermissions]

    def get_object(self, pk):
        obj = get_object_or_404(Projects, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def list(self, request):
        queryset = Projects.objects.filter(contributors=request.user)
        serializer = ProjectsSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        project = self.get_object(pk)
        serializer = ProjectsSerializer(project)
        return Response(serializer.data)

    def create(self, request):
        data = request.data.dict()
        data['contributors'] = [request.user.pk]
        data['author'] = request.user.pk
        serializer_data = ProjectsSerializer(data=data)
        serializer_data.is_valid(raise_exception=True)
        serializer_data.save()
        return Response(serializer_data.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        project = self.get_object(pk)
        serializer = ProjectsSerializer(project, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk=None):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, data={'message': 'bien effacé'})


class UserProjectsViewSet(viewsets.ViewSet):
    """
        Actions for project's collaborators
        'GET' = List project's collaborators
        'POST' = Add user in project's collaborators
        'DELETE' = Remover user in project's collaborators
    """

    permission_classes = [UserPermissions]

    def get_object(self, pk):
        obj = get_object_or_404(Projects, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def list(self, request, projects_pk=None):
        project = self.get_object(projects_pk)
        serializer = UsersProjectSerializer(project)
        return Response(serializer.data)

    def create(self, request, projects_pk=None):
        project = self.get_object(projects_pk)
        project.contributors.add(int(request.data.dict()['contributors']))
        serializer = ProjectsSerializer(project)
        return Response(serializer.data)

    def destroy(self, request, projects_pk=None, pk=None):
        project = self.get_object(projects_pk)
        project.contributors.remove(pk)
        serializer = ProjectsSerializer(project)
        return Response(serializer.data)


class IssuesProjectsViewSet(viewsets.ViewSet):
    """
        Actions for project's issue
        'GET' = List project's issues
        'POST' = Add issue in project
        'PUT' = Modify issue 
        'DELETE' = Delete issue
    """

    permission_classes = [IssueCommentPermissions]

    def get_object(self, project_pk=None, pk=None):
        if pk == None:
            obj = get_object_or_404(Projects, pk=project_pk)
        else:
            obj = get_object_or_404(Issues, pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def list(self, request, projects_pk=None):
        project = self.get_object(projects_pk)
        issues = Issues.objects.filter(project_id=project.pk)
        serializer = IssuesSerializer(issues, many=True)
        return Response(serializer.data)

    def create(self, request, projects_pk=None):
        project = self.get_object(projects_pk)
        data = request.data.dict()
        data['project'] = project.pk
        data['author'] = request.user.pk
        data['assignee_user'] = request.user.pk
        serializer_data = IssuesSerializer(data=data)
        serializer_data.is_valid(raise_exception=True)
        serializer_data.save()
        return Response(serializer_data.data, status=status.HTTP_201_CREATED)

    def update(self, request, projects_pk=None, pk=None):
        """Update a Issue"""
        issue = self.get_object(pk=pk)
        serializer = IssuesSerializer(issue, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None, projects_pk=None):
        issue = self.get_object(pk=pk)
        issue.delete()
        return Response(status=204, data={'message': 'bien effacé'})


class CommentsIssuesViewSet(viewsets.ViewSet):
    """
        Actions for issue's comment
        'GET' = List issue's comments
        'POST' = Add comment in issue
        'PUT' = Modify comment 
        'DELETE' = Delete comment
    """
    
    permission_classes = [IssueCommentPermissions]

    def get_object(self, project_pk=None, pk=None):
        if pk == None:
            obj = get_object_or_404(Projects, pk=project_pk)
        else:
            obj = get_object_or_404(Comments, pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def issue(self, pk):
        return Issues.objects.get()

    def list(self, request, projects_pk, issues_pk):
        self.get_object(projects_pk)
        queryset = Comments.objects.filter(issue_id=issues_pk)
        serializer = CommentsSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, projects_pk, issues_pk, pk):
        self.get_object(projects_pk)
        comment = get_object_or_404(Comments, pk=pk)
        serializer = CommentsSerializer(comment)
        return Response(serializer.data)

    def create(self, request, projects_pk=None, issues_pk=None):
        self.get_object(projects_pk)
        data = request.data.dict()
        data['author_user_id'] = request.user.pk
        data['issue_id'] = issues_pk
        serializer_data = CommentsSerializer(data=data)
        serializer_data.is_valid(raise_exception=True)
        serializer_data.save()
        return Response(serializer_data.data, status=status.HTTP_201_CREATED)

    def update(self, request, projects_pk=None, issues_pk=None, pk=None):
        comment = self.get_object(pk=pk)
        serializer = IssuesSerializer(issue, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, issues_pk=None, projects_pk=None, pk=None):
        comment = self.get_object(pk=pk)
        comment.delete()
        return Response(status=204, data={'message': 'bien effacé'})
