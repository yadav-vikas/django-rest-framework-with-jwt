from django.urls import path
from . import views

urlpatterns = [
    path('', views.ExpensesListAPIVivew.as_view(), name='expenses'),
    path('<int:pk>', views.ExpenseDetailAPIView.as_view(), name="expense_id"),
]