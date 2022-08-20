from events_inpsect.blockchain_scan import BlockChainScan
from events_inpsect.web3_provider import MyWeb3
from events_inpsect.utils import get_block_by_timestamp
from events_inpsect.contract_calls import get_pair_decimals, get_erc20_decimals
from app_contract import Pair
import time


# timestamp='1602824592' difficulty='0' hash='0x2a15031ba5b90dba2ff6aa21d59273fc6f5e5b5537611301c553b7726c34abda' miner='0x0000000000000000000000000000000000000000' number=19395804 size=0 transactions_count=0 gas_used='0'
if __name__ == "__main__":

    web3 = MyWeb3('aurora').get_http_provider()


    block = get_block_by_timestamp(web3, 1660307495)
    print('block', block)


    bsc_scan = BlockChainScan(web3)

    res = get_pair_decimals(web3, '0x61C9E05d1Cdb1b70856c7a2c53fA9c220830633c')
    print(res)
    erc20 = get_erc20_decimals(web3, '0x4988a896b1227218e4A686fdE5EabdcAbd91571f')
    # print(web3.eth.get_block(71844287))



