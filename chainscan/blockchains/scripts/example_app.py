from events_inpsect.blockchain_scan import Pair, BlockChainScan
from events_inpsect.web3_provider import MyWeb3
import time



if __name__ == "__main__":

    web3 = MyWeb3('bsc').get_http_provider()


    PAIRS = (
        ('0x0eD7e52944161450477ee417DE9Cd3a859b14fD0', 'CAKE_WBNB'),
        ('0xA39Af17CE4a8eb807E076805Da1e2B8EA7D0755b', 'CAKE_USDT'),
        ('0x7EFaEf62fDdCCa950418312c6C91Aef321375A00', 'USDT_BUSD'),
        ('0x16b9a82891338f9bA80E2D6970FddA79D1eb0daE', 'BUSD_WBNB'),
        ('0x8FA59693458289914dB0097F5F366d771B7a7C3F', 'MBOX_WBNB'),
    )

    pairs = [Pair(address=p[0], symbol=p[1]) for p in PAIRS] 

    bsc_scan = BlockChainScan(web3)
    
    tik = time.time()
    blocks_range = [ [19395441, 19395441+500] for _ in range(len(PAIRS))]
    # pairs_data = bsc_scan.get_scan_event_from_blocks(blocks_range, pairs)
    pairs_data = bsc_scan.get_scan_event_from_blocks_async(blocks_range, pairs)
    print('time', time.time() - tik)
    print('pairs:', len(pairs_data))
    print('events:', sum([len(pair) for pair in pairs_data]))

    # can make dict with key and data
    pairs_dict = { PAIRS[i][1]:pairs_data[i] for i in range(len(pairs_data)) }

