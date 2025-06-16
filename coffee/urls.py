from django.contrib import admin
from django.urls import path, include
from coffee.views import *
from coffee.apiviews import router
from django.conf.urls import *
import re

urlpatterns = [
    path("", index_view), 
    path("auth/", auth, name='authorization'), 
    path("api/", include(router.urls)),
    path("main/", main, name='main-window'),
    path("guide/", guide, name='guide'),
    path("guideMetrics/", guideMetrics, name='guideMetrics'),
    path("archive/", workarchive, name='archive'),
    path("profile/", profile, name='profile'),
    path("profileMetrics/", profileMetrics, name='profileMetrics'),
    path("logout/", logOutView, name="logout"),
    path("metric/<int:id>/", metric, name="metric"),
    path('save_to_archive/', save_to_archive, name='save_to_archive'),
    path('mlmodel/<int:id>/', mlmodel, name='mlmodel'),
]
