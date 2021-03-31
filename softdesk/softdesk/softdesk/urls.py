from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
											TokenObtainPairView,
											TokenRefreshView,
											)
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers


from authentification.views import RegisterView
from api.views import ProjectsViewSet, UserProjectsViewSet, IssuesProjectsViewSet, CommentsIssuesViewSet

router = DefaultRouter()
router.register(r'projects', ProjectsViewSet, basename='Projets')

projects_routers = routers.NestedSimpleRouter(router, r'projects', lookup='projects')
projects_routers.register(r'users', UserProjectsViewSet,  basename='Users_projects')
projects_routers.register(r'issues', IssuesProjectsViewSet,  basename='Issues_projects')

issues_routers = routers.NestedSimpleRouter(projects_routers, r'issues', lookup='issues')
issues_routers.register(r'comments', CommentsIssuesViewSet, basename='Comments_issues')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', RegisterView.as_view(), name='signup'),
    path('', include(router.urls)),
    path('', include(projects_routers.urls)),
    path('', include(issues_routers.urls)),

]
