
import os
from static_ranges import Ranges
from dj_static import Cling,MediaCling
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_course.settings')


application = Ranges(Cling(MediaCling(get_wsgi_application())))
