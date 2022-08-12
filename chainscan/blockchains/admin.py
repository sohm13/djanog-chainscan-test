from django.contrib import admin

from .models import BSCPair, BscEthSyncEvent, BSCBlock, AuroraPair, AuroraEthSyncEvent, AuroraBlock


class BscEthSyncEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'pair_address', 'block_number', 'updated_at')


admin.site.register(BSCBlock)
admin.site.register(BSCPair)
admin.site.register(BscEthSyncEvent, BscEthSyncEventAdmin)

admin.site.register(AuroraPair)
admin.site.register(AuroraEthSyncEvent)
admin.site.register(AuroraBlock)
