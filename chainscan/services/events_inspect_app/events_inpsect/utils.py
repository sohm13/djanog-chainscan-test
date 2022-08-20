from web3 import Web3, AsyncHTTPProvider

from typing import Optional
from .schemas import Token


def get_block_by_timestamp(web3: Web3, timestamp: int, tries: int = 100) -> Optional[int]:
    '''
        use binary search
        делает несколько попыток, в каждой попытки убвавляет (timestamp -1), 
        так как в блоке может не быть нужного времени,
        если попыток достаточно много, то гаронтирвоанно найдем нужный ближайший блок снизу
    '''
    high = web3.eth.block_number
    low = 0

    for i in range(tries):
        while low <= high:
            mid = (low + high) // 2 
            guess = web3.eth.get_block(mid)
            # print(guess.number, guess.timestamp,correct_timestamp, f'{[low, high]}')
            if guess.timestamp == timestamp:
                return mid
            if guess.timestamp > timestamp:
                high = mid - 1
            else:
                low = mid + 1
        timestamp -= 1
        # for optimisation search
        low -= 5
        high += 5
    return None


async def get_block_by_timestamp_async(web3: AsyncHTTPProvider, timestamp: int, high: int = None, low: int = None, tries: int = 100) -> Optional[int]:
    '''
        use binary search
        делает несколько попыток, в каждой попытки убвавляет (timestamp -1), 
        так как в блоке может не быть нужного времени,
        если попыток достаточно много, то гаронтирвоанно найдем нужный ближайший блок снизу
    '''
    high = await web3.eth.block_number if not high else high
    low = 0 if not low else low

    for i in range(tries):
        while low <= high:
            mid = (low + high) // 2 

            guess = await web3.eth.get_block(mid)
            # print(guess.number, guess.timestamp,correct_timestamp, f'{[low, high]}')
            if guess.timestamp == timestamp:
                return mid
            if guess.timestamp > timestamp:
                high = mid - 1
            else:
                low = mid + 1
        timestamp -= 1
        # for optimisation search
        low -= 5
        high += 5
    return None

def sort_tokens(token_a: Token, token_b: Token) -> tuple[Token, Token]:
    token0, token1 = (token_a, token_b) if int(token_a.address, 16) < int(token_b.address, 16) else (token_b, token_a)
    return (token0, token1)

