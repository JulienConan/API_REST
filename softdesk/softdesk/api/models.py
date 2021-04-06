from django.db import models
from django.conf import settings


class Projects(models.Model):

    TYPE_CHOICE = (
        ('back-end', 'back-end'),
        ('front-end', 'front-end'),
        ('iOs', 'iOs'),
        ('Android', 'Android'))

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    type = models.CharField(max_length=30, choices=TYPE_CHOICE)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='author_project')
    contributors = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL, related_name='contributors')

    def __str__(self):
        return self.title

class Issues(models.Model):

    TAG_CHOICE = (
        ('BUG', 'BUG'),
        ('AMELIORATION', 'AMELIORATION'),
        ('TACHE', 'TACHE')
    )
    PRIORITY_CHOICE = (
        ('FAIBLE', 'FAIBLE'),
        ('MOYENNE', 'MOYENNE'),
        ('ELEVEE', 'ELEVEE')
    )
    STATUT_CHOICE = (
        ('A faire', 'A faire'),
        ('En cours', 'En Cours'),
        ('Terminé', 'Termine')
    )

    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=1024)
    tag = models.CharField(max_length=30, choices=TAG_CHOICE)
    priority = models.CharField(max_length=30, choices=PRIORITY_CHOICE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='project')
    statut = models.CharField(max_length=30, choices=STATUT_CHOICE)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE, related_name='author_issue')
    assignee_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comments(models.Model):

    description = models.CharField(max_length=1024)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issues, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
