# Generated by Django 5.0.6 on 2025-01-14 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_coursepurchased_mail_delivered'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursepurchased',
            name='customer_status',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]