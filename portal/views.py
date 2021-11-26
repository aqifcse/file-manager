import datetime
from django.contrib import messages
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
from django.views.generic import ListView
from django.db.models import Q
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.http import is_safe_url
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, render_to_response

from .forms import AdminAuthForm, FileUploadForm
from .models import File

from rest_framework.views import APIView


class AppDeleteAPIView(APIView):
    
    def post(self, request):
        entry_id = request.POST.get('app_name') # Here app_name in the AJAX hold the entry_id

        app = get_object_or_404(App, pk=entry_id)

        count = File.objects.filter(app__app_name = app).count() - 1 # By clicking delete button one count is already decreased
        
        if (count < 1): # When an app has no other instance lef but itself, excute the following
            File.objects.filter(id=entry_id).delete()
            AppAuthor.objects.filter(app_name = app).delete()  

        else: # If an app has other versions left
            File.objects.filter(id=entry_id).delete()
            # When a version of an App is deleted, the last inactive version will be activated 
            version = File.objects.filter(app__app_name=app)    
            last_version = 0
            for v in version:
                if last_version < v.app_version_code:
                    last_version = v.app_version_code
                v.save()
            App.objects.filter(app__app_name=app, app_version_code = last_version).update(is_active = True)

        return Response({
            'status': status.HTTP_202_ACCEPTED,
            'message': 'File deleted.'
        })

class AdminLoginView(LoginView):
    form_class = AdminAuthForm

    def get_success_url(self):
        if self.request.user:
            return reverse('portal:home')
        else:
            return reverse('portal:home')

    def form_invalid(self, form):
        # error message
        error_messages = []
        message = form.errors.get_json_data()
        for _, message_value in message.items():
            error = message_value[0]['message']
            error_messages.append(error)
        message_ = ' And '.join(error_messages)

        # Check user_type
        user_type = 'asdfa'
        if user_type:
            messages.error(self.request, message_)
            return redirect('admin_login')
        elif user_type:
            messages.error(self.request, message_)
            return redirect('admin_login')
        return self.render_to_response(self.get_context_data(form=form))

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        url_is_safe = is_safe_url(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ''

class DashboardView(ListView):
    template_name = 'portal/home.html'
    context_object_name = 'files'
    ordering = ['date']

    def get_queryset(self):

        queryset = {
        }
        return queryset

def file_upload(request):
    if request.method == 'POST':
        aul_form = FileUploadForm(request.POST, request.FILES, instance=request.user)
        try:
            author = request.user.username
            author_name = User.objects.get(user__username=author)

            if aul_form.is_valid():
                app_file = aul_form.cleaned_data['app_file']
                app_logo = aul_form.cleaned_data['app_logo']
                app_name = aul_form.cleaned_data['app_name']  
                app_version_name = aul_form.cleaned_data['app_version_name']
                app_short_description = aul_form.cleaned_data['app_short_description']
                app_long_description = aul_form.cleaned_data['app_long_description']
                app_release_note = aul_form.cleaned_data['app_release_note']
                app_update_notice = aul_form.cleaned_data['app_update_notice']

                if app_file.name.endswith('.apk'):
                    app_file.name =  unquote(app_name).replace(' ', '_') + '_' + 'version' + '_' + app_version_name + '.apk'
                    
                else:
                    messages.error(request, 'Please upload APK file', extra_tags = 'apk_ext')
                    return render(request, 'portal/file_upload.html', { 'aul_form': aul_form })

                if not app_logo or app_logo==None:
                    messages.error(request, 'Insert a logo in jpg or png', extra_tags = 'logo_empty')
                    return render(request, 'portal/file_upload.html', { 'aul_form': aul_form })

                elif not app_logo.name.endswith(('jpg', 'png', 'jpeg', 'JPG', 'JPEG', 'PNG')):
                    messages.error(request, 'Only jpg or png is supported format for logo', extra_tags = 'logo_ext')
                    return render(request, 'portal/file_upload.html', { 'aul_form': aul_form })

                if App.objects.filter(app__app_name = app_name).exists():
                    messages.error(request, 'same app name already exist', extra_tags = 'app_name_exist')
                    return render(request, 'portal/file_upload.html', { 'aul_form': aul_form })
                
                fs = FileSystemStorage()
            
                file = fs.save( 'apk/' + unquote(app_file.name).replace(' ', '_'), app_file)
        
                # the fileurl variable now contains the url to the file. This can be used to serve the file when needed. 
                fileurl = unquote(fs.url(file)).replace(' ', '_')

                apk = APK(settings.BASE_DIR+fileurl)

                app_version_code = int(apk.version_code)

                app_package_name = apk.package
                if App.objects.filter(app_package_name = app_package_name).exists():
                    messages.error(request, 'App name with the same package name already exist', extra_tags = 'package_name_exist')
                    return render(request, 'portal/file_upload.html', { 'aul_form': aul_form })

                AppAuthor.objects.create(author=author_name, app_name=app_name)
                app = AppAuthor.objects.get(app_name=app_name)

                App.objects.create(
                    app_file=fileurl.replace('/media',''),
                    app_logo=app_logo,
                    app=app, 
                    app_version_code=app_version_code, 
                    app_version_name=app_version_name, 
                    app_package_name=app_package_name, 
                    app_short_description=app_short_description, 
                    app_long_description=app_long_description,
                    app_release_note=app_release_note,
                    app_update_notice=app_update_notice,    
                )
                
                return redirect('portal:app-developer-app-list')
        
            else:
                messages.error( request, 'Invalid Input', extra_tags = 'form_invalid' )
                return render(request, 'portal/file_upload.html', { 'aul_form': aul_form })

        except:
            messages.error( request, 'Form Crashed', extra_tags = 'form_crashed' )
            return render(request, 'portal/file_upload.html', { 'aul_form': aul_form })
    else:
        aul_form = FileUploadForm(instance=request.user)
        return render(request, 'portal/file_upload.html', { 'aul_form': aul_form })

class UploadedFileView(ListView):
    model = File
    template_name = 'portal/file_list.html'
    context_object_name = 'files'
    paginate_by = 10

    def get_queryset(self):
        author = self.request.user.username
        author_name = AppDeveloper.objects.get(user__username=author)
        form = self.request.GET.get('q')
        if form:
            return App.objects.filter(
                Q(app__app_name__icontains=form) | 
                Q(app_version_code__icontains=form) |
                Q(app_version_name__icontains=form) |
                Q(app_package_name__icontains=form) | 
                Q(app_short_description__icontains=form)
            ).order_by('pub_date').reverse()
        queryset = App.objects.filter(app__author=author_name).order_by('pub_date').reverse()
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['q'] = self.request.GET.get('q')
        return super().get_context_data(**kwargs)