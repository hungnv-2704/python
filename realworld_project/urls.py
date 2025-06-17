from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    # path('api/v1/', include(('myapp.urls_v1', 'v1'), namespace='v1')),
    # path('api/v2/', include(('myapp.urls_v2', 'v2'), namespace='v2')),
]
