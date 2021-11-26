from django.db import models
from django.template.defaultfilters import slugify

from django.contrib.auth.models import AbstractUser
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import User

from django.core.validators import FileExtensionValidator
from django.contrib.contenttypes.fields import GenericRelation
from django_cleanup.signals import cleanup_post_delete
from sorl.thumbnail import delete

from django.db.models import Func

class User(AbstractUser):
    pass

class File(models.Model):
    file = models.FileField(
        upload_to='files/', 
        default=None, 
        blank = False,
    )
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'

