from django.contrib import admin
from .models import Deposite,Transactions,Crypto_for_payments
# Register your models here.

admin.site.register(Deposite)
admin.site.register(Transactions)
admin.site.register(Crypto_for_payments)
