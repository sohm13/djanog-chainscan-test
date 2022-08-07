from django.contrib import admin

from .models import BSCPair, BSCPairTransaction, BscEthSyncEvent


admin.site.register(BSCPair)
admin.site.register(BSCPairTransaction)
admin.site.register(BscEthSyncEvent)
