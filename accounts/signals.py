# signals.py
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import User
from .models import UserSession


@receiver(post_save, sender=User)
def create_user_session(sender, instance, created, **kwargs):
    if created:
        UserSession.objects.create(user=instance, session_id='')


@receiver(pre_delete, sender=User)
def delete_user_session(sender, instance, **kwargs):
    UserSession.objects.filter(user=instance).delete()
