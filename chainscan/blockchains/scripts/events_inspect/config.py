from os import getenv

# avalibale networks
NETWORKS = {
    'bsc': {
        'http_url': 'https://bsc-dataseed.binance.org/',
        'ws_url': f'wss://bsc--mainnet--ws.datahub.figment.io/apikey/{getenv("DATAHUB_KEY")}'
        
    }
}