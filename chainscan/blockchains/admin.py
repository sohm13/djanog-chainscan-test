from django.contrib import admin

from .models import BSCPair, BSCPairTransaction, BscEthSyncEvent


class BscEthSyncEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'pair_address', 'block_number', 'updated_at')


admin.site.register(BSCPair)
admin.site.register(BSCPairTransaction)
admin.site.register(BscEthSyncEvent, BscEthSyncEventAdmin)
