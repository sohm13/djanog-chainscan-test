from events_inpsect.blockchain_scan import Pair, BlockChainScan
from events_inpsect.web3_provider import MyWeb3
from events_inpsect.helper import get_pairs_config, get_pairs
from events_inpsect.utils import get_block_by_timestamp
import time




if __name__ == "__main__":

    network_name = 'bsc'

    web3 = MyWeb3(network_name).get_http_provider()

    pair_params = get_pairs_config(network_name)


    pairs_dex = get_pairs(web3, pair_params.tokens_other, pair_params.tokens_mixin, pair_params.factories)
    pairs = [Pair(address=pd.address, symbol=pd.label) for pd in pairs_dex]
    scan = BlockChainScan(web3)

    # for p in pairs_dex:
    #     print(p)
    tik = time.time()
    timestamp_start = 1655000000
    block_start = get_block_by_timestamp(web3, timestamp_start)
    block_end = get_block_by_timestamp(web3, timestamp_start+100)
    blocks_range = [ [block_start, block_end] for _ in range(len(pairs))]
    pairs_data = scan.get_scan_event_from_blocks(blocks_range, pairs)
    # pairs_data = scan.get_scan_event_from_blocks_async(blocks_range, pairs)
    print('time', time.time() - tik)
    print('pairs:', len(pairs_data))
    print('events:', sum([len(pair) for pair in pairs_data]))

    # # can make dict with key and data
    # pairs_dict = { PAIRS[i][1]:pairs_data[i] for i in range(len(pairs_data)) }


    # # blocks data
    # tik = time.time()
    # blocks = bsc_scan.get_blocks(*blocks_range[0])
    # # for b in blocks:
    # #     print(b.number, b.timestamp, b.size, len(b.transactions))
    # print(f'time for get blocks {len(blocks)}', time.time() - tik)
    # print(blocks[0])


