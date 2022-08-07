from web3 import Web3
from .decode import abi_decode

from .schemas import SyncEvent

from web3._utils.filters import Filter
from web3.types import (
    LogReceipt,
    )


class EventLogsId:
    Sync = "0x1c411e9a96e071241c2f21f7726b17ae89e3cab4c78be50e062b03a9fffbbad1" # Sync(uint112,uint112)
    Swap = "0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822"

class EthEvent:
    def __init__(self, web3: Web3):
        self.w3 = web3

    def pars_sync_event(self, event: LogReceipt)->SyncEvent:
        reserves = abi_decode(['uint112', 'uint112'], event.data)
        return SyncEvent(
            reserve0 = reserves[0],
            reserve1 = reserves[1],
            hash = event.transactionHash.hex(),
            block_number = event.blockNumber,
            transaction_index = event.transactionIndex,
            pair_address = event.address,
            method = event.topics[0].hex(),
        )

    def sync_event(self, pair_address) -> Filter:
        return self.w3.eth.filter({
            'address':pair_address,
            "topics":[
                EventLogsId.Sync,
            ]
        })

    def sync_event_from_blocks_filter(self, pair_address: str, block_start:int, block_end: int) -> Filter:
        return self.w3.eth.filter({
            'address':pair_address,
            'fromBlock': block_start,
            'toBlock': block_end,
            "topics":[
                EventLogsId.Sync,
            ]
        })