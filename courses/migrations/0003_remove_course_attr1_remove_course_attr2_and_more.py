# Generated by Django 4.2.4 on 2023-08-27 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_coursemaster_filetype_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='attr1',
        ),
        migrations.RemoveField(
            model_name='course',
            name='attr2',
        ),
        migrations.RemoveField(
            model_name='course',
            name='attr3',
        ),
        migrations.RemoveField(
            model_name='course',
            name='attr4',
        ),
        migrations.RemoveField(
            model_name='course',
            name='attr5',
        ),
        migrations.RemoveField(
            model_name='course',
            name='attr6',
        ),
        migrations.RemoveField(
            model_name='coursepurchased',
            name='attr1',
        ),
        migrations.RemoveField(
            model_name='coursepurchased',
            name='attr2',
        ),
        migrations.RemoveField(
            model_name='coursepurchased',
            name='attr3',
        ),
        migrations.RemoveField(
            model_name='coursepurchased',
            name='attr4',
        ),
        migrations.RemoveField(
            model_name='coursepurchased',
            name='attr5',
        ),
        migrations.RemoveField(
            model_name='coursepurchased',
            name='attr6',
        ),
        migrations.AlterField(
            model_name='course',
            name='course_image',
            field=models.ImageField(blank=True, null=True, upload_to='course_images/'),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_master',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='courses.coursemaster'),
        ),
        migrations.AlterField(
            model_name='course',
            name='demo_video',
            field=models.FileField(blank=True, null=True, upload_to='course_demo'),
        ),
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='discount',
            field=models.CharField(blank=True, default=0, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='totalprice',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='coursemaster',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='coursemaster',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='course_images/'),
        ),
        migrations.AlterField(
            model_name='coursepurchased',
            name='discount',
            field=models.CharField(blank=True, default=0, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='coursepurchased',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='coursepurchased',
            name='quantity',
            field=models.PositiveIntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='filetype',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='videofiles',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='videoinstructions',
            name='instruction',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='videoinstructions',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
