from django.core.management.base import BaseCommand
from django.utils import timezone

from blockchains.models import BSCPair, BscEthSyncEvent, BSCBlock

from blockchains.scripts.events_inspect.blockchain_scan import BlockChainScan
from blockchains.scripts.events_inspect.web3_provider import MyWeb3
from blockchains.scripts.events_inspect.schemas import Pair




class Command(BaseCommand):
    
    INIT_BLOCK = 19395440

    def handle(self, *args, **options):

        pairs = BSCPair.objects.all()

        pairs_block_range = []
        last_block = self.INIT_BLOCK + 500
        step = 5

        #########################
        # get last update block in pair from db
        for pair in pairs:
            pair_sync = BscEthSyncEvent.objects.filter(pair_address = pair.pair_address).last()
            block_start = self.INIT_BLOCK

            if pair_sync:
                block_start = pair_sync.block_number + 1

            block_end = block_start + step if block_start + step < last_block else last_block
            pairs_block_range.append([block_start, block_end])            

        # prepare data for request to blockchain
        pairs_requests = [Pair(address = pair.pair_address, symbol = pair.pair_symbol) for pair in pairs]

        print('pairs', pairs)
        print('pairs_block_range', pairs_block_range)

        ###
        bsc = BlockChainScan(MyWeb3('bsc').get_http_provider())

        # get logs data from blockhain
        pairs_events = bsc.get_scan_event_from_blocks_async(pairs_block_range, pairs_requests)
        assert len(pairs_events) == len(pairs), '"update_balance" len(pairs_events) == len(pairs)'

        #########################
        # get blocks data from db
        blocks_qs = BSCBlock.objects.all()
        last_block_number_in_blocks = blocks_qs.last().number if blocks_qs.last() else self.INIT_BLOCK

        block_end = max(map(lambda r: r[1], pairs_block_range))
        print('last_block_number_in_blocks', last_block_number_in_blocks, block_end)
        if last_block_number_in_blocks < block_end:
            # get blocks data from blockhain for update db
            blocks_chain = bsc.get_blocks(
                        block_start = last_block_number_in_blocks + 1,
                        block_end = block_end
                        )
            # update blocks data in db
            data_blocks_for_db_save = [BSCBlock(**block.dict()) for block in blocks_chain]
            obj = BSCBlock.objects.bulk_create(data_blocks_for_db_save)
            # get updated data drom bd
            blocks_qs = BSCBlock.objects.all()


        #########################
        # save data to bd in BscEthSyncEvent table 
        data_for_db_save = []
        blocks_check = []
        for (pair, pair_events) in zip(pairs, pairs_events):
            events_for_db = [
                BscEthSyncEvent(**event.dict(), 
                                updated_at=timezone.now(),
                                bsc_pair=pair,
                                bsc_block=blocks_qs.get(number=event.block_number)
                                ) 
                for event in pair_events if event
                ]

            blocks_check = [event.block_number for event in pair_events]
            data_for_db_save.extend(events_for_db)
        
        for i in range(len(data_for_db_save)):
            assert data_for_db_save[i].block_number == blocks_check[i], 'dont correct db_udpate'
        
        # for d in data_for_db_save:
        #     print('d',d.block_number, d.bsc_block, d.bsc_pair)
        obj = BscEthSyncEvent.objects.bulk_create(data_for_db_save)

        self.stdout.write(f"Pairs updaed, len data {len(data_for_db_save)}" )
