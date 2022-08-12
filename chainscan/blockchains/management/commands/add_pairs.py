# from re import T
import sys
from django.core.management.base import BaseCommand
from django.utils import timezone

from blockchains.models import BSCPair, BscEthSyncEvent, BSCBlock

from blockchains.scripts.events_inspect.blockchain_scan import BlockChainScan
from blockchains.scripts.events_inspect.web3_provider import MyWeb3
from blockchains.scripts.events_inspect.contract_calls import get_pair_address, get_pair_decimals
# from blockchains.scripts.events_inspect.schemas import Pair
from blockchains.scripts.events_inspect.config import NETWORKS


from itertools import product, combinations
from dataclasses import dataclass


@dataclass
class Token:
    address: str
    label: str

@dataclass
class Factory:
    address: str
    label: str

@dataclass
class SkipToken:
    tokena_address: str
    tokenb_address: str
    factory_address: str

@dataclass
class Pair:
    address: str
    label: str
    token0: Token
    token1: Token
    factory: Factory
    decimals: int = 18



def get_pairs_config(network_name: str = 'bsc') -> dict:
    network = NETWORKS[network_name]
    tokens = network['tokens']
    factories = [ Factory(address=v, label=k) for k,v in network['factories'].items()]
    token_mixin = [ Token(address=tokens[token_name], label=token_name) for token_name in network['generate_pair_params']['tokens_mixin_list']]
    token_other = [ Token(address=tokens[token_name], label=token_name) for token_name in network['generate_pair_params']['tokens_other_list']]
    return {
        'factories': factories,
        'tokens_mixin': token_mixin,
        'tokens_other': token_other
    }


# TOKENS_MIXIN = [
#     Token(address='0x55d398326f99059ff775485246999027b3197955', label='USDT'),
#     Token(address='0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c', label='WBNB'),
#     Token(address='0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d', label='USDC'),
#     Token(address='0x2170Ed0880ac9A755fd29B2688956BD959F933F8', label='ETH'),
# ]

# TOKENS = [
#     Token(address='0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82', label='CAKE'),
#     Token(address='0x0D8Ce2A99Bb6e3B7Db580eD848240e4a0F9aE153', label='FIL'),
#     Token(address='0xbA2aE424d960c26247Dd6c32edC70B295c744C43', label='DOGE'),
# ]

# FACTORIES = [
#     Factory(address='0xca143ce32fe78f1f7019d7d551a6402fc5350c73', label='pancakeswap'),
#     Factory(address='0x858e3312ed3a876947ea49d572a7c42de08af7ee', label='biswap'),
# ]




def _make_token_pairs(tokens: list[Token], tokens_mixin: list[Token]) -> list[tuple[Token, Token]]: #
    mixin_pairs = list(combinations(tokens_mixin, 2))
    tokens_pairs = list(product(tokens, tokens_mixin))
    tokens_pairs.extend(mixin_pairs)
    return tokens_pairs

def get_pairs(
        web3: MyWeb3, tokens: list[Token],
        tokens_mixin: list[Token], factories: list[Factory],
        skip_tokens_list: list[SkipToken] = []
        ) -> list[Pair]:
    tokens_pairs = _make_token_pairs(tokens, tokens_mixin)
    pairs = []
    for factory in factories:
        for token0, token1 in tokens_pairs:
            
            is_black_list = False
            for skip_token in skip_tokens_list:
                # check via plurality
                cur_address =  [token0.address.lower(), token1.address.lower(), factory.address.lower()]
                skip_address = [skip_token.tokena_address.lower(), skip_token.tokenb_address.lower(), skip_token.factory_address.lower()]
                uniq_address = set(cur_address +  skip_address)
                if len(uniq_address) == 3:
                    is_black_list = True
                    continue
            if is_black_list:
                continue

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
            f.write(f'{pair.factory.address},{pair.address},{pair.label},{pair.token0.address},{pair.token1.address},{pair.decimals}\n')




class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        network_name = 'aurora'
        print('network_name', network_name)
        pairs_config = get_pairs_config(network_name)
        TOKENS = pairs_config['tokens_other']
        TOKENS_MIXIN = pairs_config['tokens_mixin']
        FACTORIES = pairs_config['factories']


        qs_pairs = BSCPair.objects.all()

        skip_tokens = [SkipToken(
            tokenb_address = qs_pair.token0,
            tokena_address = qs_pair.token1,
            factory_address = qs_pair.factory_address
        ) for qs_pair in qs_pairs ]

        web3 = MyWeb3(network_name).get_http_provider()
        new_pairs = get_pairs(web3, TOKENS, TOKENS_MIXIN, FACTORIES, skip_tokens)

        pairs_prepare_for_db = [
                BSCPair(
                        factory_address = pair.factory.address, 
                        pair_address = pair.address, 
                        token0 = pair.token0.address,
                        token1 = pair.token1.address,
                        factory_symbol = pair.factory.label, 
                        pair_symbol = pair.label,
                        token0_symbol = pair.token0.label,
                        token1_symbol = pair.token1.label,

                        decimals = pair.decimals,
                       updated_at = timezone.now()
                       ) 
                for pair in new_pairs
                ]
        BSCPair.objects.bulk_create(pairs_prepare_for_db)

        self.stdout.write(f"Pairs added {[p.pair_symbol for p in pairs_prepare_for_db]}" )
