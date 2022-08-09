from events_inpsect.web3_provider import MyWeb3
from events_inpsect.contract_calls import get_pair_address, get_pair_decimals
import time
import json

from itertools import product, permutations
from dataclasses import dataclass, asdict

@dataclass
class Token:
    address: str
    label: str

@dataclass
class Factory:
    address: str
    label: str

@dataclass
class Pair:
    address: str
    label: str
    token0: Token
    token1: Token
    factory: Factory
    decimals: int = 18


TOKENS_MIXIN = [
    Token(address='0x55d398326f99059ff775485246999027b3197955', label='USDT'),
    Token(address='0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c', label='WBNB'),
    Token(address='0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d', label='USDC'),
    Token(address='0x2170Ed0880ac9A755fd29B2688956BD959F933F8', label='ETH'),
]

TOKENS = [
    Token(address='0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82', label='CAKE'),
    Token(address='0x0D8Ce2A99Bb6e3B7Db580eD848240e4a0F9aE153', label='FIL'),
]

FACTORIES = [
    Factory(address='0xca143ce32fe78f1f7019d7d551a6402fc5350c73', label='pancakeswap'),
    Factory(address='0x858e3312ed3a876947ea49d572a7c42de08af7ee', label='biswap'),

]


def get_pairs(web3: MyWeb3, tokens: list[Token], tokens_mixin: list[Token], factories: list[Factory]) -> list[Pair]:
    mixin_pairs = list(permutations(tokens_mixin, 2))
    tokens_pairs = list(product(tokens, tokens_mixin))
    tokens_pairs.extend(mixin_pairs)
    pairs = []
    for factory in factories:
        for token0, token1 in tokens_pairs:
            pair_address = get_pair_address(web3, token0.address, token1.address, factory.address)
            if pair_address[:2] != '0x' or int(pair_address, 16) == 0:
                continue
            decimals = get_pair_decimals(web3, pair_address)
            pairs.append(Pair(
                address = pair_address,
                label = f'{token0.label}_{token1.label}',
                token0 = token0,
                token1 = token1,
                factory = factory,
                decimals = decimals
            ))
    return pairs

def pairs_to_csv(pairs: list[Pair], file_name: str = 'pairs') -> None:
    with open(file_name + '.csv', 'w') as f:
        for pair in pairs:
            f.write(f'{pair.address},{pair.label},{pair.token0.address},{pair.token1.address},{pair.decimals}\n')





if __name__ == '__main__':
    # web3 = MyWeb3('bsc').get_http_provider()
    web3 = MyWeb3('bsc').get_ws_provider()


    tik = time.time()

    pairs = get_pairs(web3, TOKENS,TOKENS_MIXIN, FACTORIES)
    pairs_to_csv(pairs)
    print('time:', time.time() - tik)
    
