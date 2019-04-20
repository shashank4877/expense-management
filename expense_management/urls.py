"""expense_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib.auth.decorators import login_required
from django.urls import path

from django.conf.urls import include
from django.contrib import admin
from django.views.generic.base import TemplateView
from rest_framework_swagger.views import get_swagger_view

from core.views import ExpenseView, ExpenseViewSet, profile
from rest_framework.routers import DefaultRouter

from django.conf import settings
from django.conf.urls.static import static


api_router = DefaultRouter()
api_router.register(r'expense', ExpenseViewSet, 'expense')
admin.autodiscover()


schema_view = get_swagger_view(title='Expense Tracker API')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',TemplateView.as_view(template_name="base.html")),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', login_required(TemplateView.as_view(template_name="accounts/profile.html"))),
    path('api-auth/', include('rest_framework.urls')),
    path('add-expense/', login_required(ExpenseView.as_view())),
    path('edit-expense/<str:id>/', login_required(ExpenseView.as_view())),
    path('v1/', include(api_router.urls)),
    path('expense-list/', login_required(ExpenseView.expense_list)),
    path('expense-docs/', schema_view)
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

