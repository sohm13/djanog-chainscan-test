import asyncio
import logging
import concurrent.futures
import time

from web3 import Web3
from web3._utils.filters import Filter
from web3.types import (
    LogReceipt,
     Optional,
     BlockData
    )

from .schemas import SyncEvent, Pair, Block
from .events import EthEvent, EventLogsId

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s  - %(message)s')
logger = logging.getLogger(__name__)






class BlockChainScan:
    poll_interval = 1

    def __init__(self, web3: Web3):
        self.w3: Web3 = web3
        self.eth_event: EthEvent = EthEvent(self.w3)

    

    def get_sync_events(self, block_events: list[LogReceipt]) -> list[SyncEvent]:
        events_return = []
        for event in block_events:
            sync_event = self.eth_event.pars_sync_event(event)
            events_return.append(sync_event)
        return events_return


    async def get_sync_events_async(self, block: Filter) -> list[SyncEvent] :
        block_events = block.get_all_entries()
        events_return = self.get_sync_events(block_events)
        return events_return

    async def get_scan_event_from_blocks_async(self, pairs_block_range: list[list], pairs: list[Pair]) -> list[list[Optional[SyncEvent]]]:
        '''
        DONT WORK
        return [ 
                [blocks SyncEvent], # pair[0]
                [blocks SyncEvent], # pair[1]
                ...
                ]
        '''
        tasks = [self.eth_event.get_sync_logs_async(pair.address, block_range[0], block_range[1]) 
                    for pair, block_range in zip(pairs, pairs_block_range
                    )]

        tx_sync_logs: list[LogReceipt] = await asyncio.gather(*tasks)
        sync_events = [self.get_sync_events(tx_sync_log) for tx_sync_log in tx_sync_logs]
        return sync_events

    async def get_scan_event_from_blocks_one_bunch_async(self, block_start, block_end, pairs: list[Pair], block_batch_size: int = 5000) -> list[Optional[SyncEvent]]:
        pairs_address = [p.address for p in pairs]
        logs: list[LogReceipt] = []
        for block in range(block_start, block_end, block_batch_size):
            batch_start = block if block == block_start else block + 1
            batch_end = min(block + block_batch_size, block_end)
            _logs = await self.eth_event.get_sync_logs_async(pairs_address, batch_start, batch_end)
            logs.extend(_logs)
        sync_events = self.get_sync_events(logs)
        return sync_events


    def get_scan_event_from_blocks(self, pairs_block_range: list[list], pairs: list[Pair]) -> list[list[Optional[SyncEvent]]]:
        blocks = [self.eth_event.sync_event_from_blocks_filter(pair.address, block_range[0], block_range[1]) 
                    for pair, block_range in zip(pairs, pairs_block_range
                    )]
        pairs_event_logs = []
        for i, block in enumerate(blocks):
            block_events = block.get_all_entries()
            _sync_events = self.get_sync_events(block_events)
            pairs_event_logs.append(_sync_events)
        return pairs_event_logs
    


    def get_blocks(self, block_start: int, block_end: int) -> list[Block]:
        blocks_data = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            blocks_data = executor.map(self.w3.eth.get_block, range(block_start, block_end+1))
        blocks = [Block(
                timestamp = block.timestamp,
                difficulty = block.difficulty,
                hash = block.hash.hex(),
                miner = block.miner,
                number = block.number,
                size = block.size,
                transactions_count = len(block.transactions),
                gas_used = block.gasUsed
        ) for block in blocks_data]
        return blocks

    async def get_blocks_async(self, block_start: int, block_end: int, requests_limit_per_min: int = None) -> list[Block]:
        blocks_data = []
        if requests_limit_per_min:
            block_batch_size = requests_limit_per_min
            for block in range(block_start, block_end, block_batch_size):
                batch_start = block if block == block_start else block + 1
                batch_end = min(block + block_batch_size, block_end)
                tasks = [self.w3.eth.get_block(i) for i in range(batch_start, batch_end)]
                _blocks_data = await asyncio.gather(*tasks)
                blocks_data.extend(_blocks_data)
                if block + block_batch_size < block_end:
                    await asyncio.sleep(60)
        else:          
            tasks = [self.w3.eth.get_block(i) for i in range(block_start, block_end)]
            blocks_data = await asyncio.gather(*tasks)

        blocks = [Block(
                timestamp = block.timestamp,
                difficulty = block.difficulty,
                hash = block.hash.hex(),
                miner = block.miner,
                number = block.number,
                size = block.size,
                transactions_count = len(block.transactions),
                gas_used = block.gasUsed
        ) for block in blocks_data]
        return blocks

