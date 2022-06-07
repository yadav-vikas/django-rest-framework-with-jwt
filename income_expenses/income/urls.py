from django.urls import path
from . import views

urlpatterns = [
    path('', views.IncomeListAPIVivew.as_view(), name='Income'),
    path('<int:pk>', views.IncomeDetailAPIView.as_view(), name="Income_id"),
]