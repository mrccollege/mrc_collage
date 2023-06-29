# Generated by Django 4.0 on 2023-06-29 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_course_lang_course_validate_for_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='image',
        ),
        migrations.AddField(
            model_name='course',
            name='course_image',
            field=models.ImageField(default='', null=True, upload_to='course_images/'),
        ),
        migrations.AddField(
            model_name='course',
            name='demo_video',
            field=models.FileField(default='', null=True, upload_to='course_demo'),
        ),
    ]
