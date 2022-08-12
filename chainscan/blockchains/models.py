from operator import mod
from django.db import models
from datetime import  datetime



class BaseEthPair(models.Model):
    factory_address = models.CharField(max_length=42, blank=False, null=False)
    pair_address = models.CharField(max_length=42, blank=False, null=False, unique=True)
    token0 = models.CharField(max_length=42, blank=False, null=False)
    token1 = models.CharField(max_length=42, blank=False, null=False)

    pair_symbol = models.CharField(max_length=12, blank=False, null=False, unique=False)
    factory_symbol = models.CharField(max_length=42, blank=True, null=True)
    token0_symbol = models.CharField(max_length=12, blank=True, null=True)
    token1_symbol = models.CharField(max_length=12, blank=True, null=True)
    
    decimals = models.IntegerField(default=18)
    updated_at = models.DateTimeField(auto_created=True, null=True)
    
    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.pair_symbol}'


class BaseBlock(models.Model):
    timestamp = models.CharField(max_length=68, null=True)
    difficulty = models.CharField(max_length=68, null=True)
    hash = models.CharField(max_length=68, null=True)
    miner = models.CharField(max_length=42, null=True)
    number = models.IntegerField(null=True, unique=True)
    size = models.IntegerField(null=True, default=0)
    transactions_count = models.IntegerField(null=True)
    gas_used = models.CharField(max_length=68, default='0')
    
    class Meta:
        abstract = True
    
    def __str__(self):
        return f'{self.number}'


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

    def __str__(self):
        return self.pair_address


class BSCPair(BaseEthPair):
    class Meta(BaseEthPair.Meta):
        db_table = 'BSCPair'

class BSCBlock(BaseBlock):
    class Meta(BaseBlock.Meta):
        db_table = 'BSCBlock'


class BscEthSyncEvent(BaseEthSyncEvent):

    bsc_pair = models.ForeignKey("BSCPair", on_delete=models.CASCADE, null=True)
    bsc_block = models.ForeignKey("BSCBlock", on_delete=models.CASCADE, null=True)

    class Meta(BaseEthSyncEvent.Meta):
        db_table = 'BscEthSyncEvent'


## aorora netowkr 
class AuroraPair(BaseEthPair):
    class Meta(BaseEthPair.Meta):
        db_table = 'AuroraPair'

class AuroraBlock(BaseBlock):
    class Meta(BaseBlock.Meta):
        db_table = 'AuroraBlock'

class AuroraEthSyncEvent(BaseEthSyncEvent):

    pair_model = models.ForeignKey("AuroraPair", on_delete=models.CASCADE, null=True)
    block_model = models.ForeignKey("AuroraBlock", on_delete=models.CASCADE, null=True)

    class Meta(BaseEthSyncEvent.Meta):
        db_table = 'AuroraEthSyncEvent'





NETWORK_MODELS_MAP = {
        'bsc': {
            'pair_model': BSCPair,
            'eth_sync_event_model': BscEthSyncEvent,
            'block_model': BSCBlock
        },
        'aurora': {
            'pair_model': AuroraPair,
            'eth_sync_event_model': AuroraEthSyncEvent,
            'block_model': AuroraBlock,
        }
    }