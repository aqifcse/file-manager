from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from .views import DashboardView, file_upload, UploadedFileView

app_name = 'portal'

urlpatterns = [
	path('home/', DashboardView.as_view(), name='home'),
    path('file-upload/', file_upload, name='file-upload'),
    path('file-list/', UploadedFileView.as_view(), name='file-list'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
