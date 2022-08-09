from django.core.management.base import BaseCommand
from django.utils import timezone

from blockchains.models import BSCPair, BscEthSyncEvent, BSCBlock

from blockchains.scripts.events_inspect.blockchain_scan import BlockChainScan
from blockchains.scripts.events_inspect.web3_provider import MyWeb3
from blockchains.scripts.events_inspect.schemas import Pair



class Command(BaseCommand):
    
    INIT_BLOCK = 19395440

    def handle(self, *args, **options):
        pass