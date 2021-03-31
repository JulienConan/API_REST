from django.contrib import admin
from .models import Projects, Issues, Comments

class ProjectsAdmin(admin.ModelAdmin):
	pass

admin.site.register(Projects, ProjectsAdmin)
admin.site.register(Issues)
admin.site.register(Comments)
