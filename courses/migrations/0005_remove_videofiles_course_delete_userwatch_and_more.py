# Generated by Django 4.0 on 2023-07-14 05:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_course_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videofiles',
            name='course',
        ),
        migrations.DeleteModel(
            name='UserWatch',
        ),
        migrations.DeleteModel(
            name='VideoFiles',
        ),
    ]
