from operator import mod
from django.db import models
from datetime import  datetime


class BaseEthPair(models.Model):
    factory_address = models.CharField(max_length=42, blank=False, null=False)
    pair_address = models.CharField(max_length=42, blank=False, null=False, unique=True)
    pair_symbol = models.CharField(max_length=12, blank=False, null=False, unique=True)
    token0 = models.CharField(max_length=42, blank=False, null=False)
    token1 = models.CharField(max_length=42, blank=False, null=False)
    updated_at = models.DateTimeField(auto_created=True, null=True)
    
    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.pair_symbol}'


class BaseEthPairTransaction(models.Model):
    reserveToken0 = models.CharField(max_length=256, blank=False, null=False, default=0)
    reserveToken1 = models.CharField(max_length=256, blank=False, null=False, default=0)
    amount0In = models.CharField(max_length=256, blank=False, null=True)
    amount1In = models.CharField(max_length=256, blank=False, null=True)
    amount0Out = models.CharField(max_length=256, blank=False, null=True)
    amount1Out = models.CharField(max_length=256, blank=False, null=True)
    maker_address = models.CharField(max_length=42, blank=False, null=False)
    block_number = models.IntegerField(null=True, blank=False)
    hash = models.CharField(max_length=66, null=True, blank=False)
    updated_at = models.DateTimeField(auto_created=True, null=True)

    class Meta:
        abstract = True

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


class BSCPairTransaction(BaseEthPairTransaction):
    pair = models.ForeignKey(BSCPair, on_delete=models.CASCADE)

    class Meta(BaseEthPairTransaction.Meta):
        db_table = 'BSCPairTransaction'


class BscEthSyncEvent(BaseEthSyncEvent):

    bsc_pair = models.ForeignKey(BSCPair, on_delete=models.CASCADE)
    class Meta(BaseEthSyncEvent.Meta):
        db_table = 'BscEthSyncEvent'

    def __str__(self):
        return f'block_number:{self.block_number}, transaction_index:{self.transaction_index}, pair_address:{self.pair_address}'




