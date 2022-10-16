from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.forms import ImageField
import time
from account.models import CustomUser
# Create your models here.

DIFF_CHOICES_TRADE_MODE = (
    ('running','running'),
    ('pending','pending'),
    ('completed','completed'),
)

DIFF_CHOICES_TRANS_MODE = (
    ('pending','pending'),
    ('approved','approved'),
)


    

class Deposite(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    plan = models.CharField(max_length=200)
    ammount = models.FloatField()
    profit_percent = models.FloatField()
    time_count_for_trade = models.IntegerField(default=0)
    time_of_trade = models.CharField(max_length=120)
    transaction_mode = models.CharField(max_length=11,choices=DIFF_CHOICES_TRANS_MODE)
    trade_mode = models.CharField(max_length=11,choices=DIFF_CHOICES_TRADE_MODE)
    profit = models.FloatField(default=0.00)
    date_created =  models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user) +" - "+ self.plan + "-" + str(self.ammount)

    

    def save(self,*args,**kwargs):
        try:
            time= int(self.time_of_trade)
            seconds = time * 60 * 60
            if self.time_count_for_trade < seconds and self.transaction_mode == "approved":
                self.trade_mode = "running"
            elif self.time_count_for_trade >= seconds and self.transaction_mode == "approved":
                self.trade_mode = "completed"
            elif self.transaction_mode == "pending":
                self.trade_mode = "pending"
        except:
            self.trade_mode = "running"
        return super().save(*args,**kwargs)

    
    



class Transactions(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    deposite_transact = models.ForeignKey(Deposite,on_delete=models.CASCADE)
    crypto = models.CharField(max_length=200)
    crypto_address = models.CharField(max_length=200)
    ammount_in_crypto= models.FloatField()
    image_of_transact = models.ImageField(upload_to='verify_transact')
    date_created =  models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return str(self.deposite_transact) +" - "+ self.crypto + "-" + str(self.ammount_in_crypto)



class Crypto_for_payments(models.Model):
    crypto = models.CharField(max_length=200)
    crypto_address = models.CharField(max_length=200)
    network = models.CharField(max_length=200,default="none")
   
    def __str__(self):
        return str(self.crypto) +" - "+ self.crypto_address 