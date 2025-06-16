from django.contrib import admin
from coffee.models import *
from django.contrib.auth.models import *
from django.contrib.contenttypes.models import *

admin.site.register(Profile)
admin.site.register(Permission)
admin.site.register(ContentType)
admin.site.register(MLModel)
admin.site.register(Metric)
admin.site.register(ReportArchive)
# Register your models here.
