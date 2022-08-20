
from web3 import Web3
import json
from .abi import FACTORY_V2_ABI, PAIR_V2_ABI, ERC20_ABI


def get_pair_address(w3: Web3, token_a: str, token_b: str, factory: str, factory_abi: json = FACTORY_V2_ABI) -> str:
    token_a, token_b, factory = [w3.toChecksumAddress(addr)  for addr in [token_a, token_b, factory]]
    factory_contract = w3.eth.contract(address=factory, abi=factory_abi)
    pair_address = factory_contract.functions.getPair(token_a, token_b).call()
    return pair_address


def get_pair_decimals(w3: Web3, pair_address, abi: json = PAIR_V2_ABI):
    contract = w3.eth.contract(address=w3.toChecksumAddress(pair_address), abi=abi)
    decimals = contract.functions.decimals().call()
    return decimals


def get_erc20_decimals(w3: Web3, address: str) -> int:
    contract = w3.eth.contract(address=w3.toChecksumAddress(address), abi=ERC20_ABI)
    decimals = contract.functions.decimals().call()
    return decimals


def get_factory_contract(w3: Web3, factory: str, factory_abi: json = FACTORY_V2_ABI):
    factory_contract = w3.eth.contract(address=w3.toChecksumAddress(factory), abi=factory_abi)
    return factory_contract

def get_erc20_contract(w3: Web3, address: str):
    contract = w3.eth.contract(address=w3.toChecksumAddress(address), abi=ERC20_ABI)
    return contract


async def get_pair_address_async(w3: Web3, token_a: str, token_b: str, factory: str, factory_abi: json = FACTORY_V2_ABI) -> str:

    factory_contract = get_factory_contract(w3, factory)
    pair_address = await factory_contract.functions.getPair(w3.toChecksumAddress(token_a), w3.toChecksumAddress(token_b)).call()
    return pair_address

async def get_erc20_decimals_async(w3: Web3, address: str) -> int:
    contract = get_erc20_contract(w3, w3.toChecksumAddress(address))
    decimals = await contract.functions.decimals().call()
    return decimals