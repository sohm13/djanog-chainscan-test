from eth_abi import decode_abi
from binascii import unhexlify


def abi_decode(types: list[str], data: str) ->list[int]:
    assert data[:2] == '0x', '- abi_decode - data must be start from `0x`'
    data_no_0x = data[2:]
    assert len(data_no_0x) % 64 == 0 , '- abi_decode -  data_no_0x % 64 == 0'
    return decode_abi(types, unhexlify(data_no_0x))