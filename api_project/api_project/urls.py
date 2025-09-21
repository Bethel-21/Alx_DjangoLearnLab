from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # 👈 include API app routes
    path('api/token/', obtain_auth_token, name='api_token_auth'),
]
