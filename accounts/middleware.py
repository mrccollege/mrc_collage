# middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.contrib.sessions.models import Session
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from pytz import timezone as pytz_timezone
from .models import UserSession


class SingleSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            try:
                current_session_key = request.session.session_key
                current_login_time = timezone.now().astimezone(pytz_timezone('Asia/Kolkata'))
                user_sessions = UserSession.objects.filter(user=request.user)
                for user_session in user_sessions:
                    if user_session.session_id != current_session_key:
                        # Check if another session exists and it's older than the current session
                        if user_session.login_time < current_login_time:
                            Session.objects.filter(session_key=user_session.session_id).delete()
                            user_session.delete()
                        else:
                            # If the current session is older, delete it and the corresponding session in the database
                            Session.objects.filter(session_key=current_session_key).delete()
                            return
            except UserSession.DoesNotExist:
                pass

    def process_response(self, request, response):
        if hasattr(request, 'user') and request.user.is_authenticated:
            try:
                current_session_key = request.session.session_key
                user_session, created = UserSession.objects.get_or_create(user=request.user)
                user_session.session_id = current_session_key
                user_session.login_time = timezone.now().astimezone(pytz_timezone('Asia/Kolkata'))
                user_session.save()
            except UserSession.DoesNotExist:
                pass
        return response


# Define signal handler to logout previous session when a new session is created (user logged in)
@receiver(user_logged_in)
def logout_previous_sessions(sender, user, request, **kwargs):
    current_session_key = request.session.session_key
    try:
        previous_session = UserSession.objects.get(user=user)
        if previous_session.session_id != current_session_key:
            Session.objects.filter(session_key=previous_session.session_id).delete()
            previous_session.delete()
    except UserSession.DoesNotExist:
        pass
