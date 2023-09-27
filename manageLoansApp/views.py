# views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from manageLoansApp.models import UserProfile, Loan, EMI,Transaction,Payment
from django.contrib.auth.models import User
from django.db.models import Sum
from .serializers import UserProfileSerializer, LoanSerializer, TransactionSerializer, EMISerializer
from django.shortcuts import get_object_or_404
import math, uuid, calendar
from datetime import datetime, date

@api_view(['POST'])
def register_user(request):
    try:
        aadhar_id = request.GET.get('aadhar_id', None)
        name = request.GET.get('name', None)
        email = request.GET.get('email', None)
        annual_income = request.GET.get('annual_income',None)
        print(aadhar_id,annual_income)

        user_transactions = Transaction.objects.filter(user=aadhar_id)
        
        account_balance = sum([transaction.amount if transaction.transaction_type == 'CREDIT' else -transaction.amount for transaction in user_transactions])
        if account_balance >= 1000000:
            credit_score = 900
        elif account_balance <= 100000:
            credit_score = 300
        else:
            credit_score = 300 + ((account_balance - 100000) // 15000) * 10

        print(credit_score,account_balance)

        user_profile = UserProfile.objects.create(user=User.objects.create(username=aadhar_id),name=name,email=email, annual_income=annual_income,credit_score=credit_score)
        user_profile.save()

        return Response({'Error': None, 'unique user id': user_profile.user.username,'message':'User registerd successfully!'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def apply_loan(request):
    try:
        # Extract loan application data from the request
        loan_id = uuid.uuid4()
        unique_user_id = request.GET.get('unique_user_id',None)
        loan_type = request.GET.get('loan_type',None)
        loan_amount = int(request.GET.get('loan_amount',None))
        interest_rate = int(request.GET.get('interest_rate',None))
        term_period = int(request.GET.get('term_period',None))
        disbursement_date = request.GET.get('disbursement_date',None)

        user_profile = UserProfile.objects.get(user=unique_user_id)
        print(user_profile.user)
        if user_profile.credit_score < 450:
            
            return Response({'Error': 'Credit score too low for a loan application.'}, status=status.HTTP_400_BAD_REQUEST)
        if user_profile.annual_income < 150000:
            return Response({'Error': 'Annual income too low for a loan application.'}, status=status.HTTP_400_BAD_REQUEST)

        max_loan_amounts = {
            'Car': 750000,
            'Home': 8500000,
            'Education': 5000000,
            'Personal': 1000000
        }
        if int(loan_amount) > max_loan_amounts.get(loan_type, 0):
            return Response({'Error': 'Loan amount exceeds maximum allowed for this loan type.'}, status=status.HTTP_400_BAD_REQUEST)

        principal = loan_amount
        rate_of_interest = interest_rate / 100 / 12  # Monthly interest rate
        num_of_months = term_period

        # Calculate EMI
        emi = principal * rate_of_interest * math.pow(1 + rate_of_interest, num_of_months) / (math.pow(1 + rate_of_interest, num_of_months) - 1)
        
        if emi > float(user_profile.annual_income / 12) * 0.6:
            return Response({'Error': 'EMI exceeds 60% of monthly income.'}, status=status.HTTP_400_BAD_REQUEST)
        
        loan = Loan.objects.create(loan_id=loan_id,user=user_profile, loan_type=loan_type, loan_amount=loan_amount, interest_rate=interest_rate, term_period=term_period, disbursement_date=disbursement_date)

        emi_due_dates = []
        current_date = disbursement_date
        for month in range(1, num_of_months + 1):
            emi_amount = emi
            if month == num_of_months:
                emi_amount = principal + (principal * rate_of_interest)  # Last EMI can be less than regular EMIs

            emi_due_dates.append({'Date': current_date, 'Amount_due': emi_amount})
            EMI.objects.create(loan=loan, due_date=current_date, amount_due=emi_amount)
            date_object = datetime.strptime(current_date, '%Y-%m-%d').date()
            year = date_object.year + (date_object.month + 1) // 12
            month = (date_object.month + 1) % 12 or 12
            day = min(date_object.day, calendar.monthrange(year, month)[1])
            current_date = str(date(year, month, day))

        return Response({'Error': None, 'Loan_id': loan_id, 'Due_dates': emi_due_dates}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def make_payment(request):
    try:
        loan_id = request.GET.get('loan_id')
        amount_paid = request.GET.get('amount')

        existing_payment = Payment.objects.filter(loan_id=loan_id, date=date.today()).first()
        if existing_payment:
            return Response({'Error': 'Payment for this date already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        loan = Loan.objects.get(loan_id=loan_id)

        overdue_emis = EMI.objects.filter(loan=loan, due_date=date.today())
        if overdue_emis.exists():
            return Response({'Error': 'Previous EMIs are due. Please pay those first.'}, status=status.HTTP_400_BAD_REQUEST)

        Payment.objects.create(loan=loan, date=date.today(), amount=amount_paid)

        return Response({'Error': None,'message':'Payment successfull!'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_statement(request):
    try:
        loan_id = request.GET.get('loan_id')
        loan = get_object_or_404(Loan, loan_id=loan_id)

        if loan.status == 'Closed':
            return Response({'Error': 'Loan is closed, no statement available.'}, status=status.HTTP_400_BAD_REQUEST)
        
        statement = {
            'Principal_due': 0,
            'Interest_on_principal_due': 0,
            'Repayment_of_principal': 0,
            'Upcoming_transactions': []
        }

        # Calculate 
        emis = EMI.objects.filter(loan=loan)
        total_principal_due = emis.aggregate(Sum('amount_due'))['amount_due__sum'] or 0
        statement['Principal_due'] = total_principal_due
        total_interest_on_principal = statement['Principal_due'] - loan.loan_amount
        statement['Interest_on_principal_due'] = total_interest_on_principal
        total_repayment_of_principal = total_principal_due + total_interest_on_principal
        statement['Repayment_of_principal'] = total_repayment_of_principal

        # Calculate EMIs
        upcoming_emis = EMI.objects.filter(loan=loan).order_by('due_date')
        upcoming_transactions = []
        for emi in upcoming_emis:
            upcoming_transactions.append({
                'Date': emi.due_date,
                'Amount_due': emi.amount_due
            })

        statement['Upcoming_transactions'] = upcoming_transactions

        return Response({'Error': None, 'Statement': statement}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

