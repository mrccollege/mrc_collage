from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('homepage.urls'), name='homepage'),
        path('accounts/', include('accounts.urls'), name='accounts'),
        path('dashboard/', include('dashboard.urls'), name='dashboard'),
        path('courses/', include('courses.urls'), name='courses'),
        path('demo/', include('demo.urls'), name='demo'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
