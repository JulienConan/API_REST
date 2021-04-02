from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Projects, Issues, Comments
from .permissions import (
                          ProjectPermissions,
                          UserPermissions
                          )
from .serializers import(
                        ProjectsSerializer,
                        UsersProjectSerializer,
                        IssuesSerializer,
                        CommentsSerializer
                        )

<<<<<<< Updated upstream
class ProjectsViewSet(viewsets.ViewSet):
    """API Projects actions"""
=======
class ProjectsViewSet(viewsets.ModelViewSet):

>>>>>>> Stashed changes
    permission_classes = [IsAuthenticated, ProjectPermissions]
    serializer_class = ProjectsSerializer

<<<<<<< Updated upstream
    def get_object(self, pk):
        obj = get_object_or_404(Projects, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def list(self, request):
        """Project's user list"""
        queryset = Projects.objects.filter(contributors=request.user)
        serializer = ProjectsSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """one particulary project"""
        project = self.get_object(pk)
        serializer = ProjectsSerializer(project)
        return Response(serializer.data)
=======
    def get_queryset(self):
        return Projects.objects.filter(contributors=self.request.user)
>>>>>>> Stashed changes

    def create(self, request):
        data = request.data.dict()
        data['contributors'] = [request.user.pk]
        data['author'] = request.user.pk
        serializer_data = ProjectsSerializer(data=data)
        serializer_data.is_valid(raise_exception=True)
        serializer_data.save()
        return Response(serializer_data.data, status=status.HTTP_201_CREATED)

<<<<<<< Updated upstream
    def update(self, request, pk=None):
        """Update a project"""
        project = self.get_object(pk)
        serializer = ProjectsSerializer(project, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk=None):
        """Delete a project"""
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, data={'message': 'bien effacé'})


class UserProjectsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, UserPermissions]

    def project(self, pk):
        project = get_object_or_404(Projects, pk=pk)
        return project

    def list(self, request, projects_pk=None):
        project = self.project(projects_pk)
        if request.user not in project.contributors.all():
            return Response(data={'error': 'unauthorized'})
=======

class UserProjectsViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, UserPermissions]
    serializer_class = UsersProjectSerializer

    def get_queryset(self, pk):
        project = Projects.objects.get(pk=pk)
        self.check_object_permissions(self.request, project)
        return project

    def list(self, request, projects_pk=None):
        project = self.get_queryset(projects_pk)
>>>>>>> Stashed changes
        serializer = UsersProjectSerializer(project)
        return Response(serializer.data)

    def create(self, request, projects_pk=None):
<<<<<<< Updated upstream
        project = self.project(projects_pk)
=======
        project = self.get_queryset(projects_pk)
>>>>>>> Stashed changes
        project.contributors.add(int(request.data.dict()['contributors']))
        serializer = ProjectsSerializer(project)
        return Response(serializer.data)

    def destroy(self, request, projects_pk=None, pk=None):
<<<<<<< Updated upstream
        project = self.project(projects_pk)
=======
        project = self.get_queryset(projects_pk)
>>>>>>> Stashed changes
        project.contributors.remove(pk)
        serializer = ProjectsSerializer(project)
        return Response(serializer.data)


<<<<<<< Updated upstream
class IssuesProjectsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def project(self, pk):
        return Projects.objects.get(pk=pk)

    def issue(self, pk):
        issue = get_object_or_404(Issues, pk=pk)
        return issue

    def list(self, request, projects_pk=None):
        project = self.project(projects_pk)
        issues = Issues.objects.filter(project_id=projects_pk)
        serializer = IssuesSerializer(issues, many=True)
        return Response(serializer.data)
       
=======
class IssuesProjectsViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, IssueCommentPermissions]
    serializer_class = IssuesSerializer

    def get_queryset(self):
        project_pk = self.kwargs['projects_pk']
        project = get_object_or_404(Projects, pk=project_pk)
        self.check_object_permissions(self.request, project)
        return Issues.objects.filter(project=project_pk)

>>>>>>> Stashed changes
    def create(self, request, projects_pk=None):
        data = request.data.dict()
        data['project'] = projects_pk
        data['author'] = request.user.pk
        data['assignee_user'] = request.user.pk
        serializer_data = IssuesSerializer(data=data)
        serializer_data.is_valid(raise_exception=True)
        serializer_data.save()
        return Response(serializer_data.data, status=status.HTTP_201_CREATED)
<<<<<<< Updated upstream
        
    def update(self, request, projects_pk=None, pk=None):
        """Update a Issue"""
        issue = self.issue(pk)
        serializer = IssuesSerializer(issue, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        
    def delete(self, request, pk=None, projects_pk=None):
        issue = self.issue(pk)
        issue.delete()
        return Response(status=204, data={'message': 'bien effacé'})


class CommentsIssuesViewSet(viewsets.ViewSet):

    def issue(self, pk):
        return Issues.objects.get()

    def list(self, request, projects_pk, issues_pk):
        queryset = Comments.objects.filter(issue_id=issues_pk)
        serializer = CommentsSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, projects_pk, issues_pk, pk):
        comment = get_object_or_404(Comments, pk=pk)
        serializer = CommentsSerializer(comment)
        return Response(serializer.data)
=======


class CommentsIssuesViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, IssueCommentPermissions]
    serializer_class = CommentsSerializer

    def get_queryset(self):
        print(self.request.user)
        project_pk = self.kwargs['projects_pk']
        project = get_object_or_404(Projects, pk=project_pk)
        self.check_object_permissions(self.request, project)
        return Comments.objects.filter(issue=self.kwargs['issues_pk'])
>>>>>>> Stashed changes

    def create(self, request, projects_pk=None, issues_pk=None):
        data = request.data.dict()
        data['author'] = request.user.pk
        data['issue'] = issues_pk
        serializer_data = CommentsSerializer(data=data)
        serializer_data.is_valid(raise_exception=True)
        serializer_data.save()
<<<<<<< Updated upstream
        return Response(serializer_data.data, status=status.HTTP_201_CREATED)

    def update(self, request, projects_pk=None, issues_pk=None, pk=None):
        comment = get_object_or_404(Comments, pk=pk)
        serializer = IssuesSerializer(issue, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, issues_pk=None, projects_pk=None, pk=None):
        comment = get_object_or_404(queryset, pk=pk)
        comment.delete()
        return Response(status=204, data={'message': 'bien effacé'})
=======
        return Response(serializer_data.data, data={'message' : 'commentaire créé'})
>>>>>>> Stashed changes
