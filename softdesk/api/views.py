from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny

from .models import Projects, Issues, Comments
from .permission import IsAuthorOrReadOnly
from .serializers import ProjectsSerializer, UsersProjectSerializer, IssuesSerializer, CommentsSerializer
from quickstart.models import CustomUser


class ProjectsViewSet(viewsets.ViewSet):
    """API Projects actions"""
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    queryset = Projects.objects.all()

    def list(self, request):
        """Project's user list"""
        queryset = self.queryset.filter(
            author_user_id=request.user.pk) | Projects.objects.filter(contributors=request.user.pk)
        serializer = ProjectsSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """one particulary project"""
        project = get_object_or_404(self.queryset, pk=pk)
        contributors = [user for user in project.contributors.all()]
        if request.user in contributors:
            serializer = ProjectsSerializer(project)
            return Response(serializer.data)
        else:
            return Response(data={'error': 'unauthorized'})

    def create(self, request):
        data = request.data.dict()
        data['contributors'] = [request.user.pk]
        data['author_user_id'] = request.user.pk
        serializer_data = ProjectsSerializer(data=data)
        serializer_data.is_valid(raise_exception=True)
        serializer_data.save()
        return Response(serializer_data.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Update a project"""
        project = get_object_or_404(self.queryset, pk=pk)
        if request.user.pk == project.author_user_id.pk:
            serializer = ProjectsSerializer(project, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(data={'error': 'unauthorized'})

    def delete(self,request,pk=None):
        """Delete a project"""
        project = get_object_or_404(self.queryset, pk=pk)
        project.delete()
        return Response(status=204, data={'mesage' : 'bien effacé'})
    
class UserProjectsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def project(self, pk):
        queryset = Projects.objects.all()
        project = get_object_or_404(queryset, pk=pk)
        return project

    def list(self, request, projects_pk=None):
        project = self.project(projects_pk)
        if request.user.pk in project.contributors.all():
            serializer = UsersProjectSerializer(project)
            return Response(serializer.data)
        else:
            return Response(data={'error': 'unauthorized'})

    def create(self, request, projects_pk=None):
        project = self.project(projects_pk)
        print(project.author_user_id)
        if request.user == project.author_user_id:
            project.contributors.add(int(request.query_params['contributors']))
            serializer = ProjectsSerializer(project)
            return Response(serializer.data)
        else:
            return Response(data={'error': 'unauthorized'})

    def delete(self,request,projects_pk=None,pk=None):
        project = self.project(projects_pk)
        if request.user == project.author_user_id:
            project.contributors.remove(pk)
            serializer = ProjectsSerializer(project)
            return Response(serializer.data)
        else:
            return Response(data={'error': 'unauthorized'})

class IssuesProjectsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def project(self, pk):
        return Projects.objects.get(pk=pk)

    def issue(self, pk):
        queryset = Issues.objects.all()
        issue = get_object_or_404(queryset, pk=pk)
        return issue

    def list(self, request, projects_pk=None):
        project = self.project(projects_pk)
        if request.user in project.contributors.all():
            issues = Issues.objects.filter(project_id=projects_pk)
            serializer = IssuesSerializer(issues, many=True)
            return Response(serializer.data)
        else:
            return Response(data={'error': 'unauthorized'})

    def create(self, request, projects_pk=None):
        if request.user in self.project(projects_pk).contributors.all():
            data = request.query_params.dict()
            data['project_id'] = projects_pk
            data['author_user_id'] = request.user.pk
            data['assignee_user_id'] = request.user.pk
            serializer_data = IssuesSerializer(data=data)
            serializer_data.is_valid(raise_exception=True)
            serializer_data.save()
            return Response(serializer_data.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'error': 'unauthorized'})

    def update(self, request, projects_pk=None, pk=None):
        """Update a Issue"""
        issue=self.issue(pk)
        if request.user == issue.author_user_id:
            data = request.query_params.dict()
            serializer = IssuesSerializer(issue, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(data={'error': 'unauthorized'})


    def delete(self, request, pk=None, projects_pk=None):
        issue = self.issue(pk)
        issue.delete()
        return Response(status=204, data={'message' : 'bien effacé'})


class CommentsIssuesViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def issue(self, pk):
        return Issues.objects.get()


    def list(self, request, projects_pk, issues_pk):
        queryset = Comments.objects.filter(issue_id=issues_pk)
        serializer = CommentsSerializer(queryset, many=True)
        return Response(serializer.data)

        queryset = Comments.objects.all()
        comment = get_object_or_404(queryset, pk=pk)
        serializer=CommentsSerializer(comment)
        return Response(serializer.data)

    def create(self, request, projects_pk=None, issues_pk=None):
        data = request.query_params.dict()
        data['author_user_id'] = request.user.pk
        data['issue_id'] = issues_pk
        serializer_data = CommentsSerializer(data=data)
        serializer_data.is_valid(raise_exception=True)
        serializer_data.save()
        return Response(serializer_data.data, status=status.HTTP_201_CREATED)

    def update(self, request, projects_pk=None, issues_pk=None, pk=None):
        pass

    def delete(self, request, issues_pk=None, projects_pk=None, pk=None):
        queryset = Comments.objects.all()
        comment = get_object_or_404(queryset, pk=pk)
        comment.delete()
        return Response(status=204, data={'message' : 'bien effacé'})