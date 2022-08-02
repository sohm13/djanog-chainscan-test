from django.contrib import admin

from .models import BSCPair, BSCPairTransaction


admin.site.register(BSCPair)
admin.site.register(BSCPairTransaction)