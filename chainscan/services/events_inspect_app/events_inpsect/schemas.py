from pydantic import BaseModel
from dataclasses import dataclass

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


# @dataclass
class Token(BaseModel):
    address: str
    label: str
    decimals: int = None

# @dataclass
class Factory(BaseModel):
    address: str
    label: str

# @dataclass
class PairDex(BaseModel):
    address: str
    label: str
    token0: Token
    token1: Token
    factory: Factory
    decimals: int = 18

# @dataclass
class SkipToken(BaseModel):
    tokena_address: str
    tokenb_address: str
    factory_address: str

class PairParams(BaseModel):
    factories: list[Factory]
    tokens_mixin: list[Token]
    tokens_other: list[Token]
