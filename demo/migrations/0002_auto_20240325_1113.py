# Generated by Django 3.2 on 2024-03-25 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='democourse',
            name='category',
        ),
        migrations.RemoveField(
            model_name='userdemoclass',
            name='course',
        ),
        migrations.RemoveField(
            model_name='userdemoclass',
            name='course_class',
        ),
        migrations.RemoveField(
            model_name='userdemoclass',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userdemocourse',
            name='course',
        ),
        migrations.RemoveField(
            model_name='userdemocourse',
            name='user',
        ),
        migrations.DeleteModel(
            name='DemoClass',
        ),
        migrations.DeleteModel(
            name='DemoCourse',
        ),
        migrations.DeleteModel(
            name='DemoCourseCategory',
        ),
        migrations.DeleteModel(
            name='UserDemoClass',
        ),
        migrations.DeleteModel(
            name='UserDemoCourse',
        ),
    ]
