from operator import mod
from django.db import models
from datetime import  datetime


class BaseEthPair(models.Model):
    factory_address = models.CharField(max_length=42, blank=False, null=False)
    pair_address = models.CharField(max_length=42, blank=False, null=False, unique=True)
    pair_symbol = models.CharField(max_length=12, blank=False, null=False, unique=False)
    token0 = models.CharField(max_length=42, blank=False, null=False)
    token1 = models.CharField(max_length=42, blank=False, null=False)
    decimals = models.IntegerField(default=18)
    updated_at = models.DateTimeField(auto_created=True, null=True)
    
    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.pair_symbol}'


class BaseBlock(models.Model):
    timestamp = models.CharField(max_length=68)
    difficulty = models.CharField(max_length=68, null=True)
    hash = models.CharField(max_length=68)
    miner = models.CharField(max_length=42)
    number = models.IntegerField()
    size = models.IntegerField()
    transactions_count = models.IntegerField()
    gas_used = models.CharField(max_length=68)



class BaseEthSyncEvent(models.Model):
    reserve0 = models.CharField(max_length=256, blank=False, null=False, default=0)
    reserve1 = models.CharField(max_length=256, blank=False, null=False, default=0)
    hash = models.CharField(max_length=66, null=True, blank=False)
    block_number = models.IntegerField(null=True, blank=False)
    transaction_index = models.IntegerField(null=True, blank=False)
    pair_address = models.CharField(max_length=42, blank=False, null=False)
    method = models.CharField(max_length=66, blank=False, null=False)
    updated_at = models.DateTimeField(auto_created=True, null=True)
    
    class Meta:
        abstract = True


class BSCPair(BaseEthPair):
    class Meta(BaseEthPair.Meta):
        db_table = 'BSCPair'



class BscEthSyncEvent(BaseEthSyncEvent):

    bsc_pair = models.ForeignKey(BSCPair, on_delete=models.CASCADE, null=True)

    class Meta(BaseEthSyncEvent.Meta):
        db_table = 'BscEthSyncEvent'

    def __str__(self):
        return self.pair_address




