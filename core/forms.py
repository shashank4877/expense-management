import datetime

from django.forms import fields
from django import forms
from django.forms import ModelForm
from .models import Expense


class ExpenseAddForm(ModelForm):
    """
    Expense Model form is used here for passing custom css classes to template.

    """
    expense_date = fields.DateField(initial=datetime.date.today,
                                    widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 20}))
    total_amount = forms.DecimalField(decimal_places=2, max_digits=12, min_value=0.01)


    def __init__(self, *args, **kwargs):
        super(ExpenseAddForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs['class'] = 'form-control'
        self.fields['expense_date'].widget.attrs['class'] = 'form-control mydatepicker'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['expense_bill_copy'].widget.attrs['class'] = 'form-control dropify'
        self.fields['expense_bill_copy'].widget.attrs['id'] = 'input-file-disable-remove'
        self.fields['total_amount'].widget.attrs['class'] = 'form-control'


    class Meta:
        model = Expense
        fields = '__all__'
        exclude = ('user',)

