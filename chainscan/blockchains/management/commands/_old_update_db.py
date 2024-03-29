from django.core.management.base import BaseCommand
from django.utils import timezone

from blockchains.models import  NETWORK_MODELS_MAP

from services.events_inspect_app.events_inpsect.blockchain_scan import BlockChainScan
from services.events_inspect_app.events_inpsect.web3_provider import MyWeb3
from services.events_inspect_app.events_inpsect.schemas import Pair
from services.events_inspect_app.events_inpsect.config import NETWORKS
from services.events_inspect_app.events_inpsect.utils import get_block_by_timestamp

import logging
import time


log = logging.getLogger(__name__)
log.info


class Command(BaseCommand):


    INIT_TIMESTAMP = NETWORKS['init_timestamp']


    def pairs_update(self, network_name: str = 'bsc'):
        tik = time.time()
        timers = {}
        log.info(f'netowrk {network_name} start to update pair')
        pair_model = NETWORK_MODELS_MAP[network_name]['pair_model']
        block_model = NETWORK_MODELS_MAP[network_name]['block_model']
        sync_event_model = NETWORK_MODELS_MAP[network_name]['eth_sync_event_model']

        pairs = pair_model.objects.all()


        w3 = MyWeb3(network_name).get_http_provider()
        step = NETWORKS['timestamp_step']

        tik_timestamp_block = time.time()
        INIT_BLOCK = get_block_by_timestamp(w3, self.INIT_TIMESTAMP)
        last_block_db = block_model.objects.all().last()
        log.info(f'get last_block_db: {last_block_db}')
        
        last_block_timestamp = last_block_db.timestamp if last_block_db else self.INIT_TIMESTAMP
        INIT_BLOCK_END = get_block_by_timestamp(w3, int(last_block_timestamp) + step)
        timers['time_timestamp_block'] = time.time() - tik_timestamp_block
        pairs_block_range = []
        log.info(f'{time.ctime(self.INIT_TIMESTAMP)}, init_block: {INIT_BLOCK}, init_block_end: {INIT_BLOCK_END}')

        #########################
        # get last update block in pair from db
        for pair in pairs:
            pair_sync = sync_event_model.objects.filter(pair_address = pair.pair_address).last()
            block_start = INIT_BLOCK

            if pair_sync:
                block_start = pair_sync.block_number + 1

            # block_end = block_start + step # if block_start + step < last_block else last_block
            block_end = INIT_BLOCK_END if block_start < INIT_BLOCK_END else block_start+1
            blocks_limit=  NETWORKS['bunch_blocks_limit'] - (block_end - block_start)
            if blocks_limit < 0:
                block_end += blocks_limit

            pairs_block_range.append([block_start, block_end])            

        # prepare data for request to blockchain
        pairs_requests = [Pair(address = pair.pair_address, symbol = pair.pair_symbol) for pair in pairs]

        ###
        bsc = BlockChainScan(w3)

        # get logs data from blockhain
        log.info(f'pairs_requests:{len(pairs_requests)}')
        if len(pairs_requests) == 0:
            return 
        tik_scan = time.time()
        pairs_events = bsc.get_scan_event_from_blocks(pairs_block_range, pairs_requests)
        assert len(pairs_events) == len(pairs), '"update_balance" len(pairs_events) == len(pairs)'
        timers['time_scan'] = time.time() - tik_scan
        #########################
        # get blocks data from db
        blocks_qs = block_model.objects.all()
        last_block_number_in_blocks = blocks_qs.last().number + 1 if blocks_qs.last() else INIT_BLOCK

        block_end = max(map(lambda r: r[1], pairs_block_range))
        log.info(f'last_block_number_in_blocks:{last_block_number_in_blocks}, block_end:{block_end}')

        tik_get_block = time.time()
        if last_block_number_in_blocks < block_end:
            # get blocks data from blockhain for update db
            blocks_chain = bsc.get_blocks(
                        block_start = last_block_number_in_blocks,
                        block_end = block_end
                        )
            # update blocks data in db
            data_blocks_for_db_save = [block_model(**block.dict()) for block in blocks_chain]
            obj = block_model.objects.bulk_create(data_blocks_for_db_save)
            # get updated data drom bd
            blocks_qs = block_model.objects.all()
        timers['time_get_block'] = time.time() - tik_get_block


        #########################
        # save data to bd in sync_event_model table 
        tik_db_save = time.time()
        data_for_db_save = []
        for (pair, pair_events) in zip(pairs, pairs_events):
            events_for_db = [
                sync_event_model(**event.dict(), 
                                updated_at=timezone.now(),
                                pair_model=pair,
                                block_model=blocks_qs.get(number=event.block_number)
                                ) 
                for event in pair_events
                ]
            
            data_for_db_save.extend(events_for_db)

        obj = sync_event_model.objects.bulk_create(data_for_db_save)

        timers['time_all'] = time.time() - tik
        self.stdout.write(f"Pairs updaed, len data {len(data_for_db_save)} network:{network_name}, {timers}" )


    def handle(self, *args, **options):
        netowrks_name = NETWORKS['work_networks']
        while True:

            for name in netowrks_name:
                try:
                    self.pairs_update(name)
                except Exception as e:
                    log.error(f'ERROR: {e}')

            sleep = 30
            log.info(f'sleeping: {sleep}')   
            time.sleep(sleep)

