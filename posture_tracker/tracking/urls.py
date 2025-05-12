from django.urls import path
from . import views

urlpatterns = [
    path('track_pushups/', views.track_pushups, name='track_pushups'),
    path('track_squats/', views.track_squats, name='track_squats'),
    path('track_bicep_curls/', views.track_bicep_curls, name='track_bicep_curls'),
    path('track_pullups/', views.track_pullups, name='track_pullups'),
]
