from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from django.urls import path, include


schema_view = get_schema_view(
   openapi.Info(
      title="KicksAPI",
      default_version="v0.6",
      description='''
      
      An E-commerce API.
      As of now, the core functionalities all seem functional.
      Next stage of development would include working on the user profile and connecting to the main app (API)
      '''
      ,
      #terms_of_service="",
      contact=openapi.Contact(email="abdulhamidusman218@gmail.com"),
      #license=openapi.License(name="MIT License"),
   ),
   public=True,
)

urlpatterns = [
   path('admin/', admin.site.urls),
   path('api/', include('apps.core.urls')),
   path('user/', include('apps.users.urls')),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('auth/', include('djoser.urls')),
]
