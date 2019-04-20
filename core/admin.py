from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import User,ExpenseCategory,ExpenseSubCategory, Expense

admin.site.register(User, UserAdmin)
admin.site.register(Expense)
admin.site.register(ExpenseCategory)
admin.site.register(ExpenseSubCategory)

# Register your models here.
