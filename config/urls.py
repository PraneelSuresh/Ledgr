from django.contrib import admin
from django.urls import path
from finance.views import landing, about, ping_json, transaction_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing),
    path('about/', about),
    path('ping/json/', ping_json),
    path('tx/', transaction_list),
    path('broken/', nonexistent_view)
]
