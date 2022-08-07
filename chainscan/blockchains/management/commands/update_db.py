from django.core.management.base import BaseCommand
from django.utils import timezone

from blockchains.models import BSCPair, BscEthSyncEvent

from blockchains.scripts.events_inspect.blockchain_scan import BlockChainScan
from blockchains.scripts.events_inspect.web3_provider import MyWeb3
from blockchains.scripts.events_inspect.schemas import Pair




class Command(BaseCommand):
    
    INIT_BLOCK = 19395440

    def handle(self, *args, **options):

        pairs = BSCPair.objects.all()

        pairs_block_range = []
        last_block = self.INIT_BLOCK + 500
        step = 50

        for pair in pairs:
            pair_sync = BscEthSyncEvent.objects.filter(pair_address = pair.pair_address).last()
            block_start = self.INIT_BLOCK

            if pair_sync:
                block_start = pair_sync.block_number + 1

            block_end = block_start + step if block_start + step < last_block else last_block
            pairs_block_range.append([block_start, block_end])            

        pairs = BSCPair.objects.all()
        pairs_requests = [Pair(address = pair.pair_address, symbol = pair.pair_symbol) for pair in pairs]

        print('pairs', pairs)
        print('pairs_block_range', pairs_block_range)

        bsc = BlockChainScan(MyWeb3('bsc').get_http_provider())
 
        pairs_events = bsc.get_scan_event_from_blocks_async(pairs_block_range, pairs_requests)
        assert len(pairs_events) == len(pairs), '"update_balance" len(pairs_events) == len(pairs) '

        data_for_db_save = []
        for (pair, pair_events) in zip(pairs, pairs_events):
            
            events_for_db = [BscEthSyncEvent(**event.dict(), updated_at= timezone.now(), bsc_pair=pair) for event in pair_events if event]
            data_for_db_save.extend(events_for_db)
        
        obj = BscEthSyncEvent.objects.bulk_create(data_for_db_save)

        self.stdout.write(f"Pairs updaed, len data {len(data_for_db_save)}" )
