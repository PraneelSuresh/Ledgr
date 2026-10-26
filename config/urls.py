from django.contrib import admin
from django.urls import path
from finance.views import ping, echo, landing, about, ping_json, view_transactions, another_echo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ping/', ping),
    path('echo/<int:name>/', echo),
    path('', landing),
    path('about/', about),
    path('ping/json/', ping_json),
    path('tx/', view_transactions),
    path('echo/<str:name>/<int:age>', another_echo)
]
