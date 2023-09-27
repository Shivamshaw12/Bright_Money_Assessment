from django.urls import path
from manageLoansApp import views

urlpatterns = [
    path('api/register-user/', views.register_user),
    path('api/apply-loan/', views.apply_loan),
    path('api/make-payment/', views.make_payment),
    path('api/get-statement/', views.get_statement),
]
