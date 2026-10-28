from django.contrib import admin
from .models import User, Account, Category, Transaction

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("name", "kind", "user", "opening_balance", "created_at")
    list_filter = ("kind",)
    search_fields = ("name", "user__username")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "user")
    search_fields = ("name", "user__username")

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("date", "description", "category", "account", "kind", "amount", "bucket", "created_at")
    list_filter = ("kind", "bucket", "date")
    search_fields = ("description", "category__name", "acount__name")

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username","email", "is_staff", "is_active", "date_joined")
    search_fields = ("username", "email")

