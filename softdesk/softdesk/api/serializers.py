from rest_framework import serializers
from .models import Projects, Issues, Comments


class ProjectsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Projects
        fields = '__all__'

class UsersProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projects
        fields = ['contributors']

class IssuesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issues
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = '__all__'
