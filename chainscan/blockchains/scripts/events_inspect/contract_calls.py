
from web3 import Web3
import json
from .abi import FACTORY_V2_ABI, PAIR_V2_ABI


def get_pair_address(w3: Web3, token_a: str, token_b: str, factory: str, factory_abi: json = FACTORY_V2_ABI) -> str:
    token_a, token_b, factory = [w3.toChecksumAddress(addr)  for addr in [token_a, token_b, factory]]
    factory_contract = w3.eth.contract(address=factory, abi=factory_abi)
    pair_address = factory_contract.functions.getPair(token_a, token_b).call()
    return pair_address


def get_pair_decimals(w3: Web3, pair_address, abi: json = PAIR_V2_ABI):
    contract = w3.eth.contract(address=pair_address, abi=abi)
    decimals = contract.functions.decimals().call()
    return decimals
