from django.contrib import admin
from django.urls import path
from finance.views import ping

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ping/', ping)
]
