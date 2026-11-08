from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "finance"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("ping/json/", views.ping_json, name="ping_json"),
    path("transactions/view/", views.transaction_list, name="transaction_list"),
    path("transactions/new/", views.add_transaction, name="add_transaction"),
    path("categories/", views.view_categories, name="category_list"),
    path("transactions/<int:pk>/delete/", views.delete_transaction, name="delete_transaction"),
    path("transactions/<int:pk>/edit/", views.edit_transaction, name="edit_transaction"),
    path("users/register/", views.register_user, name="register_user"),
    path("login/", views.login_user, name="login_user"),
    path("logout/", views.logout_user, name="logout_user"),
    path("categories/<int:pk>/delete/", views.delete_category, name="delete_category"),
    path("categories/add/", views.add_category, name="add_category"),
    path("categories/<int:pk>/edit/", views.edit_category, name="edit_category"),
    path("accounts/view/", views.accounts_list, name="accounts_list"),
    path("accounts/new/", views.add_account, name="add_account"),
    path("accounts/<int:pk>/delete/", views.delete_account, name="delete_account"),
    path("accounts/<int:pk>/edit/", views.edit_account, name="edit_account"),
    path("dashboard/", views.view_dashboard, name="view_dashboard")
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
