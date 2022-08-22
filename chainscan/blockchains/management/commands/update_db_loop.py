from django.core.management.base import BaseCommand
from django.utils import timezone

from blockchains.models import  NETWORK_MODELS_MAP

from services.events_inspect_app.events_inpsect.blockchain_scan import BlockChainScan
from services.events_inspect_app.events_inpsect.web3_provider import MyWeb3
from services.events_inspect_app.events_inpsect.schemas import Pair
from services.events_inspect_app.events_inpsect.config import NETWORKS
from services.events_inspect_app.events_inpsect.utils import get_block_by_timestamp_async

import logging
import time
import asyncio
import platform
from aiohttp  import ClientSession


if platform.system()=='Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


log = logging.getLogger(__name__)
log.info


class Command(BaseCommand):


    INIT_TIMESTAMP = NETWORKS['init_timestamp'] 
    # dependet from the INIT_TIMESTAMP
    INIT_BLOCKS = {network: None for network in NETWORKS['work_networks']} 

    async def pairs_update_by_blocks_asunc(self, network_name: str = 'bsc', session = None) -> None:

        log.info(f'netowrk {network_name} start to update pairs')
        pair_model = NETWORK_MODELS_MAP[network_name]['pair_model']
        block_model = NETWORK_MODELS_MAP[network_name]['block_model']
        sync_event_model = NETWORK_MODELS_MAP[network_name]['eth_sync_event_model']


        w3 = MyWeb3(network_name).get_http_provider_async()
        if session:
            await w3.provider.cache_async_session(session)
        block_step = NETWORKS['block_steps'][network_name]
        block_end = await w3.eth.block_number

        if not self.INIT_BLOCKS[network_name]:
            self.INIT_BLOCKS[network_name] = await get_block_by_timestamp_async(w3, self.INIT_TIMESTAMP)
        init_block = self.INIT_BLOCKS[network_name]
        pairs = pair_model.objects.all()
        # last_block_db = block_model.objects.all().last()
        log.info(f'pairs from db: {len(pairs)}')

        #########################
        # get last update block in pair from db
        pairs_block_range = []
        for pair in pairs:
            pair_sync = sync_event_model.objects.filter(pair_address = pair.pair_address).last()
            block_start = init_block
            
            if pair_sync:
                block_start = pair_sync.block_number + 1

            # block_last_block_start_diff = last_block_db.number - block_start
            # block_end = block_start + block_step  if block_last_block_start_diff > block_step else block_last_block_start_diff
            # blocks_limit=  NETWORKS['bunch_blocks_limit'] - (block_end - block_start)
            # if blocks_limit < 0:
            #     block_end += blocks_limit

            pairs_block_range.append([block_start, block_end])  
        
        # prepare data for request to blockchain
        pairs_requests = [Pair(address = pair.pair_address, symbol = pair.pair_symbol) for pair in pairs]
        if len(pairs_requests) == 0:
            return

        # group pairs for optimisation request

        scan = BlockChainScan(w3)
        block_start_min =  min(map(lambda r: r[0], pairs_block_range))
        # block_end_max = max(map(lambda r: r[1], pairs_block_range))
        log.info(f'request: block min request: {block_start_min}, block max request: {block_end }, blcoks to scan:{block_end-block_start_min}, block_step:{block_step}')

        # pair_logs = await scan.get_scan_event_from_blocks_async(pairs_block_range, pairs_requests)
        pair_logs = await scan.get_scan_event_from_blocks_one_bunch_async(block_start_min, block_end, pairs_requests, block_step)
        #########################
        # get blocks data from db
        blocks_qs = block_model.objects.all()
        last_block_number_in_blocks = blocks_qs.last().number + 1 if blocks_qs.last() else init_block
        last_block = pair_logs[-1].block_number if pair_logs else block_end
        log.info(f' last block from db: {blocks_qs.last()}, last_block_number_in_blocks:{last_block_number_in_blocks}')
        
        if last_block_number_in_blocks < last_block:
            # get blocks data from blockhain for update db
            requests_limit_per_min = NETWORKS[network_name]['requests_limit_per_min']
            log.info(f'wait time for get_blocks ~ {(last_block-last_block_number_in_blocks) // requests_limit_per_min} min, [blocks: {last_block-last_block_number_in_blocks}, limit: {requests_limit_per_min}]')
            blocks_chain = await scan.get_blocks_async(
                        block_start = last_block_number_in_blocks,
                        block_end = last_block+1,
                        requests_limit_per_min = requests_limit_per_min
                        )
            # update blocks data in db
            data_blocks_for_db_save = [block_model(**block.dict()) for block in blocks_chain]
            log.info(f'data_blocks_for_db_save:{len(data_blocks_for_db_save)} and update block_model')
            obj = block_model.objects.bulk_create(data_blocks_for_db_save)
            # get updated data drom bd
            blocks_qs = block_model.objects.all()
        #########################


        log.info(f'update sync_event_model, last_block_db:{blocks_qs.last().number}, last_block:{last_block}, last_block_db timestamp:{blocks_qs.last().timestamp}')

        data_for_db_save = []
        for pair_log in pair_logs:
            log_for_db = sync_event_model(**pair_log.dict(),
                updated_at=timezone.now(),
                pair_model=pair_model.objects.get(pair_address=pair_log.pair_address),
                block_model=blocks_qs.get(number=pair_log.block_number)
                )
            data_for_db_save.append(log_for_db)
        log.info(f'add data to "sync_event_model"')
        sync_event_model.objects.bulk_create(data_for_db_save)

        self.stdout.write(f"Pairs {network_name} updaed, len data {len(data_for_db_save)} " )


    async def run_session(self, name):
        async with ClientSession() as session:
            await self.pairs_update_by_blocks_asunc(name, session)

    def handle(self, *args, **options):
        netowrks_name = NETWORKS['work_networks']

        while True:
            for name in netowrks_name:
                    try:
                        asyncio.run(self.run_session(name))
                    except Exception as e:
                        log.error(f'ERROR: {e}')

            sleep = 5
            log.info(f'sleeping: {sleep}')   
            time.sleep(sleep)
