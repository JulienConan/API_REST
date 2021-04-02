from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

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


class ProjectsViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, ProjectPermissions]
    serializer_class = ProjectsSerializer

    def get_queryset(self):
        return Projects.objects.filter(contributors=self.request.user)

    def create(self, request):
        data = request.data.dict()
        data['contributors'] = [request.user.pk]
        data['author'] = request.user.pk
        serializer_data = ProjectsSerializer(data=data)
        serializer_data.is_valid(raise_exception=True)
        serializer_data.save()
        return Response(serializer_data.data, status=status.HTTP_201_CREATED)

class UserProjectsViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, UserPermissions]
    serializer_class = UsersProjectSerializer

    def get_queryset(self, pk):
        project = Projects.objects.get(pk=pk)
        self.check_object_permissions(self.request, project)
        return project

    def list(self, request, projects_pk=None):
        project = self.get_queryset(projects_pk)
        serializer = UsersProjectSerializer(project)
        return Response(serializer.data)

    def create(self, request, projects_pk=None):
        project = self.get_queryset(projects_pk)
        project.contributors.add(int(request.data.dict()['contributors']))
        serializer = ProjectsSerializer(project)
        return Response(serializer.data)

    def destroy(self, request, projects_pk=None, pk=None):
        project = self.get_queryset(projects_pk)
        project.contributors.remove(pk)
        serializer = ProjectsSerializer(project)
        return Response(serializer.data)


class IssuesProjectsViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, IssueCommentPermissions]
    serializer_class = IssuesSerializer

    def get_queryset(self):
        project_pk = self.kwargs['projects_pk']
        project = get_object_or_404(Projects, pk=project_pk)
        self.check_object_permissions(self.request, project)
        return Issues.objects.filter(project=project_pk)

    def create(self, request, projects_pk=None):
        data = request.data.dict()
        data['project'] = projects_pk
        data['author'] = request.user.pk
        data['assignee_user'] = request.user.pk
        serializer_data = IssuesSerializer(data=data)
        serializer_data.is_valid(raise_exception=True)
        serializer_data.save()
        return Response(serializer_data.data, status=status.HTTP_201_CREATED)


class CommentsIssuesViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, IssueCommentPermissions]
    serializer_class = CommentsSerializer

    def get_queryset(self):
        print(self.request.user)
        project_pk = self.kwargs['projects_pk']
        project = get_object_or_404(Projects, pk=project_pk)
        self.check_object_permissions(self.request, project)
        return Comments.objects.filter(issue=self.kwargs['issues_pk'])

    def create(self, request, projects_pk=None, issues_pk=None):
        data = request.data.dict()
        data['author'] = request.user.pk
        data['issue'] = issues_pk
        serializer_data = CommentsSerializer(data=data)
        serializer_data.is_valid(raise_exception=True)
        serializer_data.save()
        return Response(serializer_data.data, data={'message' : 'commentaire créé'})

