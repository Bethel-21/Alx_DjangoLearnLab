# urls.py (in your main project folder)
from django.urls import path, include

urlpatterns = [
    path('api/', include('api.urls')),  # Ensure this is included
    ...
]
