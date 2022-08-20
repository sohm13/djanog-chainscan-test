from events_inpsect.blockchain_scan import Pair, BlockChainScan
from events_inpsect.web3_provider import MyWeb3
from events_inpsect.helper import get_pairs_config, get_pairs
from events_inpsect.utils import get_block_by_timestamp
from events_inpsect.schemas import Token, Factory, PairDex
import time




TOKENS_MIXIN = [
    Token(address='0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c', label='WBNB'),
    Token(address='0x55d398326f99059ff775485246999027b3197955', label='USDT'),

    # Token(address='0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d', label='USDC'),
    # Token(address='0x2170Ed0880ac9A755fd29B2688956BD959F933F8', label='ETH'),
]

TOKENS = [
    Token(address='0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82', label='CAKE'),
    # Token(address='0x0D8Ce2A99Bb6e3B7Db580eD848240e4a0F9aE153', label='FIL'),
]

FACTORIES = [
    Factory(address='0xca143ce32fe78f1f7019d7d551a6402fc5350c73', label='pancakeswap'),
    # Factory(address='0x858e3312ed3a876947ea49d572a7c42de08af7ee', label='biswap'),

]



def test_order_pairs(pairs_dex: list[PairDex]):
    for pair in pairs_dex:
        assert pair.token0.address < pair.token1.address, f" 'test_order_pairs',faild  pair:({pair})"
    print('test_order_pairs OK' )


if __name__ == "__main__":

    network_name = 'bsc'

    web3 = MyWeb3(network_name).get_http_provider()

    pairs = get_pairs(web3, TOKENS, TOKENS_MIXIN, FACTORIES)
    test_order_pairs(pairs)
    # scan = BlockChainScan(web3)

    # timestamp_start = 1655000000
    # block_start = get_block_by_timestamp(web3, timestamp_start)
    # block_end = get_block_by_timestamp(web3, timestamp_start+100)
    # blocks_range = [ [block_start, block_end] for _ in range(len(PAIRS))]
    # pairs_data = scan.get_scan_event_from_blocks(blocks_range, PAIRS)

