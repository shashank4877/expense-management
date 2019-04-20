from rest_framework import serializers
from drf_braces.serializers.form_serializer import FormSerializer

from core.models import Expense, ExpenseSubCategory
from .forms import ExpenseAddForm

class ExpenseSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseSubCategory
        exclude= ('logo')



class AddExpenseSerializer(serializers.ModelSerializer):
    #category = ExpenseSubCategorySerializer(view_name='title', many=True)

    class Meta:
        model = Expense
        fields = [
            'category',
            'expense_date',
            'description',
            'expense_bill_copy',
            'total_amount',
            'id',

        ]
        #exclude = ('user','created_on','updated_on','id')

    def to_representation(self, instance):
        rep = super(AddExpenseSerializer, self).to_representation(instance)
        rep['category'] = instance.category.title
        return rep