from django.urls import path, include

urlpatterns = [
    path('tracking/', include('tracking.urls')),
]
