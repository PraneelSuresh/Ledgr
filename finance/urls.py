from django.urls import path
from . import views

app_name = "finance"

urlpatterns = [
    path("about/", views.about, name="about"),
    path("ping/json/", views.ping_json, name="ping_json"),
    path("tx/", views.transaction_list, name="transaction_list"),
]
