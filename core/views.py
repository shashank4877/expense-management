import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from rest_framework import status, mixins, viewsets, permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from core.forms import ExpenseAddForm
from core.models import Expense, ExpenseSubCategory, ExpenseCategory
from core.serializers import AddExpenseSerializer

class ExpenseViewSet(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.DestroyModelMixin,
                                viewsets.GenericViewSet):


    '''
    This Viewset is used for handling list and delete operations.
    '''


    def get_queryset(self):
        return Expense.objects.all().filter(user=self.request.user)
    serializer_class = AddExpenseSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ExpenseView(APIView, LoginRequiredMixin):
    """
    ExpenseView class handles all operations like adding new expense,
    edit existing expense and list expense request.
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'expense/add_expense.html'


    def get(self,request,format=None,id=None):
        """
        :param format: method will be able to handle urls such as http://example.com/api/items/4.json
        :param id: a value will be passed in case of edit.
        :return: a form instance will be returned if it is a edit request
                else a form to add new expense will be returned.
        """
        if id:
            instance = Expense.objects.get(id=id)
            form = ExpenseAddForm(instance=instance)
        else:
            form = ExpenseAddForm()
        return Response({'form': form,})


    def post(self, request, format=None,id=None):
        """
        :param format: method will be able to handle urls such as http://example.com/api/items/4.json
        :param id: a value will be passed in case of edit.
        :return: In case of edit or a new expense there will be a redirect to list expense page.
                 In case of mobile api request serializer data with error code will  be returned.
        """
        if id:
            instance = Expense.objects.get(id=id)
            serializer = AddExpenseSerializer(instance=instance,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return redirect('/expense-list/')
        serializer = AddExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            if request.data['csrfmiddlewaretoken']:
                return redirect('/expense-list/')
            else:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            form = ExpenseAddForm(instance=request.data)
            return Response({'form': form, })


    def expense_list(request):
        """
        It is used to handle the expense list request and expense form.
        :return: expense form and list request.

        """
        form = ExpenseAddForm()
        variables = {
            'form': form
        }
        return render(request, template_name='expense/all_expense.html',context=variables)

def profile(request):
    if request.method == 'GET':
        all_category = ExpenseCategory.objects.all()
        # main = {}
        category_details = []
        for category in all_category:
            sub_category_details = {}
            sub_category_details_list = []
            sub_category_details['category'] = category.title
            for sub_category in category.expensesubcategory_set.all():
                temp = {}
                temp['total_spent'] = str(sub_category.get_category_spent(request.user))
                temp['category'] = sub_category.title
                sub_category_details_list.append(temp)
            sub_category_details['value'] = sub_category_details_list
            category_details.append(sub_category_details)
        return render(request, template_name="accounts/profile.html", context={'category_details':category_details})

# def profile(request):
#     if request.method == 'GET':
#         all_category = ExpenseSubCategory.objects.all()
#         # main = {}
#         category_details = []
#         for category in all_category:
#             temp = {}
#             temp['total_spent'] = str(category.get_category_spent(request.user))
#             temp['category'] = category.title
#             category_details.append(temp)
#         return render(request, template_name="accounts/profile.html", context={'category_details':category_details})