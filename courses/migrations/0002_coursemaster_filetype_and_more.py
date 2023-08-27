# Generated by Django 4.2.4 on 2023-08-27 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000, null=True)),
                ('description', models.TextField(null=True)),
                ('image', models.ImageField(blank=True, default='', null=True, upload_to='course_images/')),
            ],
        ),
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
            model_name='audioinstructions',
            name='course',
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
            field=models.ImageField(blank=True, default='', null=True, upload_to='course_images/'),
        ),
        migrations.AddField(
            model_name='course',
            name='course_lang',
            field=models.CharField(blank=True, default='Hindi', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='demo_video',
            field=models.FileField(blank=True, default='', null=True, upload_to='course_demo'),
        ),
        migrations.AddField(
            model_name='course',
            name='type',
            field=models.CharField(blank=True, default='common', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='validate_for',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AddField(
            model_name='videofiles',
            name='file',
            field=models.FileField(default='', upload_to='course_files'),
        ),
        migrations.AlterField(
            model_name='course',
            name='attr1',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='attr2',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='attr3',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='attr4',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='attr5',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='attr6',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='discount',
            field=models.CharField(blank=True, default=0, max_length=10),
        ),
        migrations.AlterField(
            model_name='course',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='AudioFiles',
        ),
        migrations.DeleteModel(
            name='AudioInstructions',
        ),
        migrations.AddField(
            model_name='course',
            name='course_master',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.PROTECT, to='courses.coursemaster'),
        ),
        migrations.AddField(
            model_name='videofiles',
            name='file_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='courses.filetype'),
        ),
    ]