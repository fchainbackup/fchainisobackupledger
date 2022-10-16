from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Dashboard
from deposite.models import Deposite
from django.contrib.auth.models import User
from withdrawal.models import Code,Withdrawal_transact
from account.models import CustomUser, Profile



@receiver(post_save, sender=CustomUser)
def create_dashboard(sender, instance, created, **kwargs):
    if created:
        Dashboard.objects.create(user=instance)
        Code.objects.create(user=instance)
        Profile.objects.create(user=instance,profile_name=instance.username)
        

@receiver(post_save, sender=Deposite)
def update_dashboard(sender, instance, created, **kwargs):
    user_deposite = Deposite.objects.filter(user=instance.user)
    total_deposite = 0.0
    total_profit = 0.0
    total_investment_plan = 0
    total_active_investment_plans = 0
    for invest in user_deposite:
        if invest.transaction_mode == "approved":
            total_deposite += invest.ammount
            total_profit += invest.profit
            total_investment_plan += 1
            if invest.trade_mode == "running":
                total_active_investment_plans +=1

    each_withdraw = 0
    user_withdrawals = Withdrawal_transact.objects.filter(user=instance.user)
    for amount in user_withdrawals:
        if amount.payment_mode == "approved":
            each_withdraw += amount.ammount

    total_ammount = total_deposite + total_profit - each_withdraw
    
    user_dashboard = Dashboard.objects.get(user=instance.user)
    user_dashboard.account_balance = total_ammount
    user_dashboard.total_withdrawal = each_withdraw
    user_dashboard.total_profit = total_profit
    user_dashboard.total_investment_plans = total_investment_plan
    user_dashboard.total_active_investment_plans = total_active_investment_plans
    user_dashboard.save()
