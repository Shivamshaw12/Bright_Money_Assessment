from django.contrib import admin
from manageLoansApp.models import UserProfile, Loan,EMI,Transaction,Payment

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Loan)
admin.site.register(Transaction)
admin.site.register(EMI)
admin.site.register(Payment)