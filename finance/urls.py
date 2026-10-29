from django.urls import path
from . import views

app_name = "finance"

urlpatterns = [
    path("about/", views.about, name="about"),
    path("ping/json/", views.ping_json, name="ping_json"),
    path("transactions/", views.transaction_list, name="transaction_list"),
    path("transactions/new/", views.add_transaction, name="add_transaction"),
    path("category/", views.add_category, name="add_category")
]
