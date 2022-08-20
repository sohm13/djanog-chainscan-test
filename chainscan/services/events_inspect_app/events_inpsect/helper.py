from .config import NETWORKS
from .schemas import Factory, Token, PairDex, SkipToken, PairParams
from .contract_calls import get_pair_address, get_pair_decimals, get_erc20_decimals, get_pair_address_async, get_erc20_decimals_async
from .web3_provider import MyWeb3
from .utils import sort_tokens
from web3 import AsyncHTTPProvider, Web3

from itertools import product, combinations
import asyncio


def get_pairs_config(network_name: str = 'bsc') -> PairParams:
    network = NETWORKS[network_name]
    tokens = network['tokens']
    factories = [ Factory(address=v, label=k) for k,v in network['factories'].items()]
    token_mixin = [ Token(address=tokens[token_name], label=token_name) for token_name in network['generate_pair_params']['tokens_mixin_list']]
    token_other = [ Token(address=tokens[token_name], label=token_name) for token_name in network['generate_pair_params']['tokens_other_list']]
    return PairParams(
        factories = factories,
        tokens_mixin = token_mixin,
        tokens_other = token_other
    )




def _make_token_pairs(tokens: list[Token], tokens_mixin: list[Token]) -> list[tuple[Token, Token]]: #
    mixin_pairs = list(combinations(tokens_mixin, 2))
    tokens_pairs = list(product(tokens, tokens_mixin))
    tokens_pairs.extend(mixin_pairs)
    return tokens_pairs


def get_pairs(
            web3: MyWeb3, 
            tokens: list[Token],
            tokens_mixin: list[Token], 
            factories: list[Factory],
            skip_tokens_list: list[SkipToken] = []
            ) -> list[PairDex]:
    tokens_pairs = _make_token_pairs(tokens, tokens_mixin)
    pairs = []
    for factory in factories:
        for token_a, token_b in tokens_pairs:
            token0, token1 = sort_tokens(token_a, token_b)
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
            token0.decimals = get_erc20_decimals(web3, token0.address)
            token1.decimals = get_erc20_decimals(web3, token1.address)
            pairs.append(PairDex(
                address = pair_address,
                label = f'{token0.label}_{token1.label}',
                token0 = token0,
                token1 = token1,
                factory = factory,
                decimals = decimals,
            ))
    return pairs



async def fill_pair_async(web3: AsyncHTTPProvider, token_a: Token, token_b: Token, factory: Factory) -> PairDex:
    token0, token1 = sort_tokens(token_a, token_b)
    pair_address = await get_pair_address_async(web3, token0.address, token1.address, factory.address)
    decimals = 18
    token0.decimals = await get_erc20_decimals_async(web3, token0.address)
    token1.decimals = await get_erc20_decimals_async(web3, token1.address)
    return PairDex(
        address = pair_address,
        label = f'{token0.label}_{token1.label}',
        token0 = token0,
        token1 = token1,
        factory = factory,
        decimals = decimals,
    )

def is_pair_skip_list(skip: SkipToken, skip_tokens_list: list[SkipToken]=[]) -> bool:
    is_tokens_in = False
    for skip_token in skip_tokens_list:
        # check via plurality
        cur_address =  [skip.tokena_address.lower(), skip.tokenb_address.lower(), skip.factory_address.lower()]
        skip_address = [skip_token.tokena_address.lower(), skip_token.tokenb_address.lower(), skip_token.factory_address.lower()]
        uniq_address = set(cur_address +  skip_address)
        if len(uniq_address) == 3:
            is_tokens_in = True
            continue
    return is_tokens_in

def filter_dex_pairs(pairs: list[PairDex]) -> list[PairDex]:
    filtered_dex_pairs = []
    for pair in pairs:
        if pair.address[:2] != '0x' or int(pair.address, 16) == 0:
            continue
        filtered_dex_pairs.append(pair)
    return filtered_dex_pairs

async def get_pairs_async(
            web3: MyWeb3, 
            tokens: list[Token],
            tokens_mixin: list[Token], 
            factories: list[Factory],
            skip_tokens_list: list[SkipToken] = []
            ) -> list[PairDex]:
    tokens_pairs = _make_token_pairs(tokens, tokens_mixin)
    pairs = []
    for factory in factories:
        tasks = [fill_pair_async(web3, token_a, token_b, factory) for token_a, token_b in tokens_pairs 
                    if not is_pair_skip_list(SkipToken(tokena_address=token_a.address, tokenb_address=token_b.address, factory_address=factory.address)) ]

        dex_pairs = await asyncio.gather(*tasks)
        dex_pairs_f = filter_dex_pairs(dex_pairs)
        pairs.extend(dex_pairs_f)
    return pairs



def pairs_to_csv(pairs: list[PairDex], file_name: str = 'pairs') -> None:
    with open(file_name + '.csv', 'w') as f:
        for pair in pairs:
            f.write(f'{pair.factory.address},{pair.address},{pair.label},{pair.token0.address},{pair.token1.address},{pair.decimals}\n')


