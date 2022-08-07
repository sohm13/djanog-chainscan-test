import asyncio
import logging

from web3 import Web3
from web3._utils.filters import Filter
from web3.types import (
    LogReceipt,
     Optional
    )

from .schemas import SyncEvent, Pair
from .events import EthEvent, EventLogsId

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s  - %(message)s')
logger = logging.getLogger(__name__)






class BlockChainScan:
    poll_interval = 1

    def __init__(self, web3: Web3):
        self.w3: Web3 = web3
        self.eth_event: EthEvent = EthEvent(self.w3)

    

    def get_sync_events(self, block_events: list[LogReceipt]):
        events_return = []
        for event in block_events:
            sync_event = self.eth_event.pars_sync_event(event)
            events_return.append(sync_event)
        return events_return


    async def get_sync_events_async(self, block: Filter) -> list[SyncEvent] :
        block_events = block.get_all_entries()
        events_return = self.get_sync_events(block_events)
        return events_return

    def get_scan_event_from_blocks_async(self, block_start: int, block_end: int, pairs: list[Pair]) -> list[list[Optional[SyncEvent]]]:
        '''
        return [ 
                [blocks SyncEvent], # pair[0]
                [blocks SyncEvent], # pair[1]
                ...
                ]
        '''
        blocks = [self.eth_event.sync_event_from_blocks_filter(pair.address, block_start, block_end) for pair in pairs]
        tasks = [self.get_sync_events_async(block) for block in blocks]
        loop = asyncio.get_event_loop()
        try:
            pairs_event_logs: list[list[Optional[SyncEvent]]] = loop.run_until_complete(
                                                        asyncio.gather(*tasks)
                                                        )
        finally:
            loop.close()            
        return pairs_event_logs

    def get_scan_event_from_blocks(self, block_start: int, block_end: int,  pairs: list[Pair]) -> list[list[Optional[SyncEvent]]]:
        blocks = [self.eth_event.sync_event_from_blocks_filter(pair.address, block_start, block_end) for pair in pairs]

        pairs_event_logs = []
        for block in blocks:
            block_events = block.get_all_entries()
            _sync_events = self.get_sync_events(block_events)
            pairs_event_logs.append(_sync_events)
        return pairs_event_logs
        


