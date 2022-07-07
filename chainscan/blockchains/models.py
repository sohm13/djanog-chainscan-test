from operator import mod
from django.db import models
from datetime import  datetime
# Create your models here.


class BaseTransaction(models.Model):

    block_number = models.IntegerField(blank=False, null=True)
    address_from = models.CharField(max_length=128,  blank=False, null=True)
    address_to = models.CharField(max_length=128, null=True, blank=False)
    hash = models.CharField(max_length=256, null=True, blank=False)
    transaction_index = models.IntegerField(null=True, blank=False)
    data_input = models.TextField(null=True, blank=False, default='0x')
    nonce = models.IntegerField(null=True, blank=True)
    gas_used = models.PositiveBigIntegerField(null=True, blank=False)
    gas_price = models.PositiveBigIntegerField(null=True, blank=False)
    value = models.PositiveBigIntegerField(null=True, blank=False, default=0)
    status = models.IntegerField(null=True, blank=False)
    logs = models.TextField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class BSCTransaction(BaseTransaction):
    class Meta(BaseTransaction.Meta):
        db_table = 'BSCTransaction'

