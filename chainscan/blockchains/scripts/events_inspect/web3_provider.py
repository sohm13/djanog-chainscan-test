from typing import (
    Any,
    # Dict,
    # List,
    Optional,
    Sequence,
    Type,
    # TYPE_CHECKING,
    Union,
    # cast,
)
from web3 import Web3, AsyncHTTPProvider
from web3.eth import Eth
from web3.net import Net
from web3.version import Version
from web3.parity import Parity, ParityPersonal
from web3.geth import Geth, GethAdmin, GethMiner, GethPersonal, GethTxPool
from web3.testing import Testing
from web3.module import Module
from web3.middleware import geth_poa_middleware

from . import config


class MyWeb3(Web3):

    # cant rewrite class in dict if need
    web3_args = {
        'modules': {
            "eth": Eth,
            "net": Net,
            "version": Version,
            "parity": (Parity, {
                "personal": ParityPersonal,
            }),
            "geth": (Geth, {
                "admin": GethAdmin,
                "miner": GethMiner,
                "personal": GethPersonal,
                "txpool": GethTxPool,
            }),
            "testing": Testing,
            }
    }

    networks = {
        'bsc': config.NETWORKS["bsc"]
    }

    def __init__(self, network_name: str):
        self.network = self.get_network(network_name)


    def get_network(self, network_name: str):
        network = self.networks.get(network_name.lower(), None)
        assert network, f"network_name not found in {self.networks}"
        return network


    def set_web3_args(self,
                middlewares: Optional[Sequence[Any]] = None,
                modules: Optional[dict[str, Union[Type[Module], Sequence[Any]]]] = None,
        ):
        pass
    
    
    def get_web3_args(self):
        return self.web3_args

    def get_http_provider(self):
        '''
        '''
        # HTTPProvider = Web3(AsyncHTTPProvider(self.network['http_url']), **self.get_web3_args())
        HTTPProvider = Web3(Web3.HTTPProvider(self.network['http_url']), **self.get_web3_args())
        HTTPProvider.middleware_onion.inject(geth_poa_middleware, layer=0)

        return HTTPProvider

    def get_ws_provider(self):
        WebsocketProvider = Web3(Web3.WebsocketProvider(self.network['ws_url'] ))
        WebsocketProvider.middleware_onion.inject(geth_poa_middleware, layer=0)

        return WebsocketProvider


