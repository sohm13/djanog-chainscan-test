from os import getenv


# avalibale networks
NETWORKS = {
    'work_networks': ['bsc', 'aurora'],
    'init_timestamp': 1655000000, 
    'timestamp_step': 500,
    'bunch_blocks_limit': 5000,
    'bsc': {
        'http_url': f'https://bsc--mainnet--rpc-archive.datahub.figment.io/apikey/{getenv("DATAHUB_KEY")}' if getenv("DATAHUB_KEY", None) else 'https://bsc-dataseed.binance.org/',
        'ws_url': f'wss://bsc--mainnet--ws.datahub.figment.io/apikey/{getenv("DATAHUB_KEY")}' if getenv("DATAHUB_KEY", None) else None,

        'factories': {
            'pancakeswap': '0xca143ce32fe78f1f7019d7d551a6402fc5350c73',
            'biswap': '0x858e3312ed3a876947ea49d572a7c42de08af7ee',
        },
        'tokens': {
            'USDT':'0x55d398326f99059ff775485246999027b3197955',
            'WBNB':'0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c',
            'USDC':'0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d',
            'ETH':'0x2170Ed0880ac9A755fd29B2688956BD959F933F8',
            'CAKE':'0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82',
            'FIL':'0x0D8Ce2A99Bb6e3B7Db580eD848240e4a0F9aE153',
            },
        'generate_pair_params': {
            # tokens_mixin_list include in all combinations
            'tokens_mixin_list': ['USDT', 'WBNB', 'USDC', 'ETH'],
            'tokens_other_list': ['CAKE', 'FIL']
        }
        
    },
    'aurora': {
        'http_url': 'https://mainnet.aurora.dev',
        'ws_url': 'wss://mainnet.aurora.dev',
        
        'factories': {
            'trisolaris':'0xc66F594268041dB60507F00703b152492fb176E7',
            'wannaswap':'0x7928D4FeA7b2c90C732c10aFF59cf403f0C38246',
        },
        'tokens': {
            'WETH': '0xC9BdeEd33CD01541e1eeD10f90519d2C06Fe3feB',
            'TRI': '0xFa94348467f64D5A457F75F8bc40495D33c65aBB',
            'NEAR': '0xC42C30aC6Cc15faC9bD938618BcaA1a1FaE8501d',
            'USDC': '0xB12BFcA5A55806AaF64E99521918A4bf0fC40802',
            'USDT': '0x4988a896b1227218e4A686fdE5EabdcAbd91571f',
            'BSTN': '0x9f1F933C660a1DC856F0E0Fe058435879c5CCEf0',
            'AURORA': '0x8BEc47865aDe3B172A928df8f990Bc7f2A3b9f79',
            'DAI': '0xe3520349F477A5F6EB06107066048508498A291b',
            'WANNA': '0x7faA64Faf54750a2E3eE621166635fEAF406Ab22',
            'AVAX': '0x80A16016cC4A2E6a2CACA8a4a498b1699fF0f844',

        },
        'generate_pair_params': {
            # tokens_mixin_list include in all combinations
            'tokens_mixin_list': ['USDT', 'WETH', 'USDC'],
            'tokens_other_list': ['BSTN', 'AURORA', 'AVAX', 'TRI', 'WANNA', 'DAI']
        }
    }
}