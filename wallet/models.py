import uuid
from django.db import models
from django.contrib.auth.models import User


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.user.username
    
class Transaction(models.Model):

    TRANSACTION_TYPE = {
        ('credit', 'Credit'),
        ('debit', 'Debit')
    }

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    # transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    transaction_id = models.CharField(max_length=255, unique=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id
