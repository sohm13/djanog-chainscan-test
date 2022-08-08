from pydantic import BaseModel


class Pair(BaseModel):
    address: str
    symbol: str


class SyncEvent(BaseModel):
    reserve0: int = 0
    reserve1: int = 0
    hash: str = '0x'
    block_number: int = 0
    transaction_index: int = 0
    pair_address: str = ''
    method: str = ''


class Block(BaseModel):
    timestamp: str
    difficulty: str
    hash: str
    miner: str
    number: int
    size: int
    transactions_count: int
    gas_used: str