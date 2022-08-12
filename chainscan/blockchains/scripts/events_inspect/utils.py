from web3 import Web3

from typing import Optional


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



