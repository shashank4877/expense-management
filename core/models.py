import uuid
from datetime import date
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext as _
from django_userforeignkey.models.fields import UserForeignKey


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(_('Contact phone'), max_length=10, null=True, blank=True)
    profile_pic = models.FileField()

    def get_total_spent(self):
        try:
            total = 0
            for expense in self.expense_set.all():
                total += expense.total_amount
            return total
        except:
            return None

    def get_today_spent(self):
        try:
            total = 0
            for expense in self.expense_set.all():
                if expense.expense_date == date.today():
                    total += expense.total_amount
            return total
        except:
            return None

    def profile_data(self):
        all_category = ExpenseCategory.objects.all()
        # main = {}
        category_details = []
        for category in all_category:
            sub_category_details = {}
            sub_category_details_list = []
            sub_category_details['category'] = category.title
            for sub_category in category.expensesubcategory_set.all():
                temp = {}
                temp['total_spent'] = str(sub_category.get_category_spent(self))
                temp['category'] = sub_category.title
                sub_category_details_list.append(temp)
            sub_category_details['value'] = sub_category_details_list
            category_details.append(sub_category_details)
        return category_details


class ExpenseCategory(models.Model):
    title = models.CharField(max_length=15)

    def __str__(self):
        return self.title


class ExpenseSubCategory(models.Model):
    expense_category = models.ForeignKey(ExpenseCategory,on_delete=models.CASCADE)
    title = models.CharField(max_length=15)
    logo = models.FileField()

    def __str__(self):
        return self.title

    def get_category_spent(self,user):
        try:
            total = 0
            for expense in self.expense_set.all().filter(user=user):
                if expense.category.id == self.id:
                    total += expense.total_amount
            return total
        except:
            return None

class Expense(models.Model):
    user = UserForeignKey(auto_user_add=True,)
    category = models.ForeignKey(ExpenseSubCategory, on_delete=models.CASCADE)
    expense_date = models.DateField()
    description = models.TextField(null=True,blank=True)
    expense_bill_copy = models.FileField(null=True,blank=True)
    total_amount = models.DecimalField(decimal_places=2, max_digits=12)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
            return self.user.first_name +''+self.category.title + ' ' + str(self.total_amount)




