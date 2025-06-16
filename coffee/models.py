from django.db import models
from django.contrib.auth.models import User
# Create your models here.u

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name="profile")
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

    

class MLModel(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(User, related_name="mlmodels")
    quality = models.FloatField(default=0)
    tip1 = models.TextField(blank=True, null=True)
    tip2 = models.TextField(blank=True, null=True)
    tip3 = models.TextField(blank=True, null=True)

class Metric(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(User, related_name="metrics")
    workspace_url = models.CharField(max_length=50, blank=True, null=True)
    tip1 = models.TextField(blank=True, null=True)
    tip2 = models.TextField(blank=True, null=True)
    tip3 = models.TextField(blank=True, null=True)

class ReportArchive(models.Model):
    REPORT_TYPES = [
        ('graph', 'График'),
        ('report', 'Отчёт'),
        ('forecast', 'Прогноз')
    ]

    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    report_type = models.CharField(max_length=10, choices=REPORT_TYPES)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='old_reports/')
    filters = models.JSONField(blank=True, null=True)  
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='archives')

    def __str__(self):
        return f"{self.title} ({self.report_type})"
