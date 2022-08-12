from django.core.management.base import BaseCommand
from django.utils import timezone

from blockchains.models import  NETWORK_MODELS_MAP

from blockchains.scripts.events_inspect.blockchain_scan import BlockChainScan
from blockchains.scripts.events_inspect.web3_provider import MyWeb3
from blockchains.scripts.events_inspect.schemas import Pair
from blockchains.scripts.events_inspect.config import NETWORKS
from blockchains.scripts.events_inspect.utils import get_block_by_timestamp

import logging



log = logging.getLogger(__name__)
log.info


class Command(BaseCommand):

    


    INIT_BLOCK = NETWORKS['init_block']
    INIT_TIMESTAMP = NETWORKS['init_timestamp']

    def pairs_update_by_timestamp(self, network_name: str = 'bsc'):
        pass

    def pairs_update(self, network_name: str = 'bsc'):
        print(f'netowrk {network_name} start to update pair')
        pair_model = NETWORK_MODELS_MAP[network_name]['pair_model']
        block_model = NETWORK_MODELS_MAP[network_name]['block_model']
        sync_event_model = NETWORK_MODELS_MAP[network_name]['eth_sync_event_model']

        pairs = pair_model.objects.all()


        # INIT_BLOCK = get_block_by_timestamp()
        pairs_block_range = []
        # last_block = self.INIT_BLOCK + 500
        step = 100

        #########################
        # get last update block in pair from db
        for pair in pairs:
            pair_sync = sync_event_model.objects.filter(pair_address = pair.pair_address).last()
            block_start = self.INIT_BLOCK

            if pair_sync:
                block_start = pair_sync.block_number + 1

            block_end = block_start + step # if block_start + step < last_block else last_block
            pairs_block_range.append([block_start, block_end])            

        # prepare data for request to blockchain
        pairs_requests = [Pair(address = pair.pair_address, symbol = pair.pair_symbol) for pair in pairs]

        # print('pairs', pairs)
        # print('pairs_block_range', pairs_block_range)

        ###
        bsc = BlockChainScan(MyWeb3(network_name).get_http_provider())

        # get logs data from blockhain
        log.info(f'pairs_requests:{len(pairs_requests)}')
        pairs_events = bsc.get_scan_event_from_blocks(pairs_block_range, pairs_requests)
        # pairs_events = bsc.get_scan_event_from_blocks_async(pairs_block_range, pairs_requests)
        assert len(pairs_events) == len(pairs), '"update_balance" len(pairs_events) == len(pairs)'

        #########################
        # get blocks data from db
        blocks_qs = block_model.objects.all()
        last_block_number_in_blocks = blocks_qs.last().number if blocks_qs.last() else self.INIT_BLOCK

        block_end = max(map(lambda r: r[1], pairs_block_range))
        # print('last_block_number_in_blocks', last_block_number_in_blocks, block_end)
        log.info(f'last_block_number_in_blocks:{last_block_number_in_blocks}, block_end:{block_end}')

        if last_block_number_in_blocks < block_end:
            # get blocks data from blockhain for update db
            blocks_chain = bsc.get_blocks(
                        block_start = last_block_number_in_blocks + 1,
                        block_end = block_end
                        )
            # update blocks data in db
            data_blocks_for_db_save = [block_model(**block.dict()) for block in blocks_chain]
            obj = block_model.objects.bulk_create(data_blocks_for_db_save)
            # get updated data drom bd
            blocks_qs = block_model.objects.all()


        #########################
        # save data to bd in sync_event_model table 
        data_for_db_save = []
        for (pair, pair_events) in zip(pairs, pairs_events):

            events_for_db = [
                sync_event_model(**event.dict(), 
                                updated_at=timezone.now(),
                                bsc_pair=pair,
                                bsc_block=blocks_qs.get(number=event.block_number)
                                ) 
                for event in pair_events
                ]
            
            data_for_db_save.extend(events_for_db)

        obj = sync_event_model.objects.bulk_create(data_for_db_save)

        self.stdout.write(f"Pairs updaed, len data {len(data_for_db_save)} network:{network_name}" )


    def handle(self, *args, **options):
        netowrks_name = NETWORKS['work_networks']
        [self.pairs_update(name) for name in netowrks_name]

