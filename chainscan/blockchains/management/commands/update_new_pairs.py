from django.core.management.base import BaseCommand
from django.utils import timezone
import time
import asyncio
from web3 import Web3, AsyncHTTPProvider


from blockchains.models import NETWORK_MODELS_MAP

from services.events_inspect_app.events_inpsect.web3_provider import MyWeb3
from services.events_inspect_app.events_inpsect.schemas import SkipToken, Pair
from services.events_inspect_app.events_inpsect.config import NETWORKS
from services.events_inspect_app.events_inpsect.blockchain_scan import BlockChainScan
from services.events_inspect_app.events_inpsect.helper import get_pairs_config, get_pairs_async
from services.events_inspect_app.events_inpsect.utils import get_block_by_timestamp_async


import logging
import time


log = logging.getLogger(__name__)
log.info


async def get_pairs_data(w3: AsyncHTTPProvider, pairs: list[Pair], block_start: int, block_end: int, block_bunch: int = 5000):
       pass



class Command(BaseCommand):

    INIT_TIMESTAMP = NETWORKS['init_timestamp']
    INIT_BLOCKS = {network: None for network in NETWORKS['work_networks']} 

    async def update_new_pairs_async(self, network_name: str = 'bsc'):
        log.info('----------------------------------------------------------------')
        log.info(f'network_name {network_name}')
        pairs_config = get_pairs_config(network_name)
        TOKENS = pairs_config.tokens_other
        TOKENS_MIXIN = pairs_config.tokens_mixin
        FACTORIES = pairs_config.factories

        pair_model = NETWORK_MODELS_MAP[network_name]['pair_model']
        block_model = NETWORK_MODELS_MAP[network_name]['block_model']
        sync_event_model = NETWORK_MODELS_MAP[network_name]['eth_sync_event_model']


        qs_pairs = pair_model.objects.filter(pair_updated=False)
        log.info(f'new pairs for update: {len(qs_pairs)}')
        if len(qs_pairs) == 0:
            return None
        web3: AsyncHTTPProvider = MyWeb3(network_name).get_http_provider_async()

        scan = BlockChainScan(web3)
        pairs = [Pair(address=pd.pair_address, symbol=pd.pair_symbol) for pd in qs_pairs]

        if not self.INIT_BLOCKS[network_name]:
            self.INIT_BLOCKS[network_name] = await get_block_by_timestamp_async(web3, self.INIT_TIMESTAMP) 

        init_block = self.INIT_BLOCKS[network_name]
        block_step = NETWORKS['block_steps'][network_name]

        block_start = init_block
        last_block = await web3.eth.block_number
        last_block_init = last_block
        log.info(f'init_block:{init_block}, last_block_init:{last_block_init}], blocks:{last_block - init_block}, step: {block_step} ')
        while True: 
            pair_logs = await scan.get_scan_event_from_blocks_one_bunch_async(block_start, last_block, pairs, block_step)
            block_start = last_block + 1
            last_block = await web3.eth.block_number
            log.info(f' last_block-last_block_init:{last_block - last_block_init}, last_block_init: {last_block_init}, last_block: {last_block}')
            if last_block - last_block_init < block_step:
                break
        log.info(f' got logs:{len(pair_logs)}')

        #########################
        # get blocks data from db
        blocks_qs = block_model.objects.all()
        last_block_number_in_blocks = blocks_qs.last().number + 1 if blocks_qs.last() else init_block
        last_block = pair_logs[-1].block_number if pair_logs else last_block_init
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


        log.info(f'update sync_event_model, last_block_db:{blocks_qs.last().number}, last_block:{last_block}')

        data_for_db_save = []
        for pair_log in pair_logs:
            log_for_db = sync_event_model(**pair_log.dict(),
                updated_at=timezone.now(),
                pair_model=pair_model.objects.get(pair_address=pair_log.pair_address),
                block_model=blocks_qs.get(number=pair_log.block_number)
                )
            data_for_db_save.append(log_for_db)


        for qs_pair in qs_pairs:
            qs_pair.pair_updated = True

        log.info(f'update pair_model "pair_updated to True"')
        pair_model.objects.bulk_update(qs_pairs, ['pair_updated'])
        log.info(f'add data to "sync_event_model"')
        sync_event_model.objects.bulk_create(data_for_db_save)


        self.stdout.write(f"Update New {network_name} Pairs Done" )


    def handle(self, *args, **options):
        netowkr_names = NETWORKS['work_networks']

        for network_name in netowkr_names:
            asyncio.run(self.update_new_pairs_async(network_name))

