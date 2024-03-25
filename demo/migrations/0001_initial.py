# Generated by Django 3.2 on 2024-03-25 04:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0005_coursepurchased_coupon_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='DemoClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_file_title', models.CharField(max_length=1000, null=True)),
                ('class_file', models.FileField(default='', upload_to='demo_class_files')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DemoCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=1000, null=True)),
                ('course_image', models.ImageField(blank=True, null=True, upload_to='demo_course_images/')),
                ('course_video', models.FileField(blank=True, null=True, upload_to='demo_course_video')),
                ('course_instructor', models.CharField(blank=True, max_length=1000, null=True)),
                ('course_description', models.TextField(blank=True, null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DemoCourseCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=1000, null=True)),
                ('category_description', models.TextField(blank=True, null=True)),
                ('category_image', models.ImageField(blank=True, null=True, upload_to='demo_course_cat_image/')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserDemoCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demo.democourse')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserDemoClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('watch_count', models.IntegerField(default=0)),
                ('status', models.CharField(default='pending', max_length=25)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demo.userdemocourse')),
                ('course_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demo.democlass')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='democourse',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='demo.democoursecategory'),
        ),
        migrations.AddField(
            model_name='democlass',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demo.democourse'),
        ),
        migrations.AddField(
            model_name='democlass',
            name='file_formate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.filetype'),
        ),
    ]
