# Generated by Django 3.1.7 on 2021-03-26 08:44

from django.db import migrations
import quickstart.manager


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
                ('objects', quickstart.manager.UserManager()),
            ],
        ),
    ]
