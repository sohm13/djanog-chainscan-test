from django.core.management.base import BaseCommand
from blockchains.models import BSCPair

from scripts.events_inspect.blockchain_scan import BlockChainScan
from scripts.events_inspect.web3_provider import MyWeb3
from scripts.events_inspect.schemas import Pair


class Command(BaseCommand):
    
    INIT_BLOCK = 1939000

    def handle(self, *args, **options):

        pairs = BSCPair.objects.all()

        


        self.stdout.write("Create pairs")
