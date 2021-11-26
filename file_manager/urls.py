from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
from portal.views import AdminLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', AdminLoginView.as_view(template_name='portal/login-admin.html'), name='admin_login'),
    path('', include('portal.urls', namespace='portal')),
]
