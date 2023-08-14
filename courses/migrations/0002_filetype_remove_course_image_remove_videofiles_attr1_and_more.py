# Generated by Django 4.0 on 2023-08-12 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_type', models.CharField(max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='course',
            name='image',
        ),
        migrations.RemoveField(
            model_name='videofiles',
            name='attr1',
        ),
        migrations.RemoveField(
            model_name='videofiles',
            name='attr2',
        ),
        migrations.RemoveField(
            model_name='videofiles',
            name='attr3',
        ),
        migrations.RemoveField(
            model_name='videofiles',
            name='attr4',
        ),
        migrations.RemoveField(
            model_name='videofiles',
            name='attr5',
        ),
        migrations.RemoveField(
            model_name='videofiles',
            name='attr6',
        ),
        migrations.RemoveField(
            model_name='videofiles',
            name='video_file',
        ),
        migrations.AddField(
            model_name='course',
            name='course_image',
            field=models.ImageField(default='', null=True, upload_to='course_images/'),
        ),
        migrations.AddField(
            model_name='course',
            name='course_lang',
            field=models.CharField(default='Hindi', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='demo_video',
            field=models.FileField(default='', null=True, upload_to='course_demo'),
        ),
        migrations.AddField(
            model_name='course',
            name='type',
            field=models.CharField(default='common', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='validate_for',
            field=models.IntegerField(default=1, null=True),
        ),
        migrations.DeleteModel(
            name='AudioFiles',
        ),
        migrations.AddField(
            model_name='videofiles',
            name='file_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='courses.filetype'),
        ),
    ]