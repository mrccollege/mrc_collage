# Generated by Django 5.0.6 on 2024-12-06 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_rename_delivery_status_coursepurchased_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursemaster',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='course_master_video'),
        ),
    ]