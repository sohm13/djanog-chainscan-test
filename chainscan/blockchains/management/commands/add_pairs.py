from django.core.management.base import BaseCommand
from django.utils import timezone
import time

from blockchains.models import NETWORK_MODELS_MAP

from services.events_inspect_app.events_inpsect.web3_provider import MyWeb3
from services.events_inspect_app.events_inpsect.schemas import SkipToken
from services.events_inspect_app.events_inpsect.config import NETWORKS
from services.events_inspect_app.events_inpsect.helper import get_pairs_config, get_pairs_async

import logging
import asyncio

log = logging.getLogger(__name__)
log.info


class Command(BaseCommand):

    async def add_pairs_async(self, network_name: str = 'bsc'):
        tik = time.time()
        log.info('--------------------')
        log.info(f'network_name {network_name}' )
        print(f'network_name {network_name}' )
        pairs_config = get_pairs_config(network_name)
        TOKENS = pairs_config.tokens_other
        TOKENS_MIXIN = pairs_config.tokens_mixin
        FACTORIES = pairs_config.factories

        pair_model = NETWORK_MODELS_MAP[network_name]['pair_model']

        qs_pairs = pair_model.objects.all()
        skip_tokens = [SkipToken(
            tokenb_address = qs_pair.token0,
            tokena_address = qs_pair.token1,
            factory_address = qs_pair.factory_address
        ) for qs_pair in qs_pairs ]

        web3 = MyWeb3(network_name).get_http_provider_async()
        new_pairs = await get_pairs_async(web3, TOKENS, TOKENS_MIXIN, FACTORIES, skip_tokens)
        print(f'new pairs: {len(new_pairs)}')
        if len(new_pairs) == 0:
            print('not new pairs')
            return None

        pairs_prepare_for_db = [
                pair_model(
                        factory_address = pair.factory.address, 
                        pair_address = pair.address, 
                        token0 = pair.token0.address,
                        token1 = pair.token1.address,
                        factory_symbol = pair.factory.label, 
                        pair_symbol = pair.label,
                        token0_symbol = pair.token0.label,
                        token1_symbol = pair.token1.label,

                        decimals = pair.decimals,
                        token0_decimals = pair.token0.decimals,
                        token1_decimals = pair.token1.decimals,
                       updated_at = timezone.now()
                       ) 
                for pair in new_pairs
                ]
        pair_model.objects.bulk_create(pairs_prepare_for_db)

        self.stdout.write(f"Pairs added {[p.pair_symbol for p in pairs_prepare_for_db]}, time:{time.time() - tik}" )


    def handle(self, *args, **options):
        netowkr_names = NETWORKS['work_networks']

        for network_name in netowkr_names:
            asyncio.run(self.add_pairs_async(network_name))

