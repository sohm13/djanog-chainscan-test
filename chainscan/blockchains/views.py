from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from django.core.paginator import Paginator
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
# from django.views.generic.edit import FormView
# from django.views.generic.base import TemplateView

import pandas as pd

from .scripts.events_inspect.blockchain_scan import BlockChainScan
from .scripts.events_inspect.web3_provider import MyWeb3
from .scripts.events_inspect.schemas import Pair


from .models import BSCPair, BSCPairTransaction, BscEthSyncEvent
from .forms import PairFiletrForm

import time

def index(request):
    return render(request, 'blockchains/index.html')


class BscListView(ListView):
    model = BSCPair
    template_name = 'blockchains/bsc_list.html'
    context_object_name = 'pairs'
    paginate_by = 10



def pair_sync_event_to_df(pair: BscEthSyncEvent, decimals=18):

        pre_to_pandas = [obj.__dict__ for obj in pair ]
        df = pd.DataFrame(pre_to_pandas)
        df['reserve0'] = df['reserve0'].astype(float) / (10 ** decimals)
        df['reserve1'] = df['reserve1'].astype(float) / (10 ** decimals)
        df['price'] = df['reserve0']/ df['reserve1']
        df['token0'] = df['reserve1'] - df['reserve1'].shift()
        df['token1'] = df['reserve0'] - df['reserve0'].shift()
        # columns for display
        df = df[[
            'block_number', 
            'transaction_index', 
            'price', 
            # 'pair_address', 
            'reserve0', 
            'reserve1',
            'token0',
            'token1',
            'hash'
            ]]
        return df


def bsc_pair_detail(request: HttpRequest, pk: int):
    
    bsc_pair = BSCPair.objects.get(pk=pk)
    pair = BscEthSyncEvent.objects.filter(bsc_pair=bsc_pair).order_by('-id')
    pair_df = pair_sync_event_to_df(pair, bsc_pair.decimals)

    context = {
        'pair_df': pair_df,
        'ticker': bsc_pair.pair_symbol,
        'address': bsc_pair.pair_address,
    }
    
    return render(request, 'blockchains/bsc_detail.html', context=context)

    

# def pair_balances(response):
#     if response.method == 'POST':
#         form = PairFiletrForm(response.POST)

#         pairs_addresses = form.data['pairs_address'].split(',')
#         block_start = int(form.data['block_start'])
#         block_end = int(form.data['block_end'])
#         pairs = [Pair(address=address, symbol=address) for address in pairs_addresses]

#         pair = BscEthSyncEvent.objects.filter(pair_address=pairs[0].address, block_number__gt=block_end)
#         pair_all = BscEthSyncEvent.objects.all()

#         response_time = 0
#         if len(pair) < 1:
#             tik = time.time()
#             bsc = BlockChainScan(MyWeb3('bsc').get_http_provider())

#             transcations = bsc.get_scan_event_from_blocks(block_start, block_end, pairs)[0]
#             response_time = time.time()-tik

#             pair = [BscEthSyncEvent(**tx.dict()) for tx in transcations if tx]
#             obj = BscEthSyncEvent.objects.bulk_create(pair)



#         pre_to_pandas = [obj.__dict__ for obj in pair ]
#         df = pd.DataFrame(pre_to_pandas)
#         #columns: ['reserve0', 'reserve1', 'hash', 'block_number', 'transaction_index', 'pair_address', 'method'],

#         # print(df.info())
#         pair_decimals = 18
#         df['reserve0'] = df['reserve0'].astype(float) / (10 ** pair_decimals)
#         df['reserve1'] = df['reserve1'].astype(float) / (10 ** pair_decimals)
#         df['price'] = df['reserve0']/ df['reserve1']
#         df['token0'] = df['reserve1'] - df['reserve1'].shift()
#         df['token1'] = df['reserve0'] - df['reserve0'].shift()
#         # columns for display
#         df = df[[
#             'block_number', 
#             'transaction_index', 
#             'price', 
#             'pair_address', 
#             'reserve0', 
#             'reserve1',
#             'token0',
#             'token1',
#             'hash'
#             ]]

#         context = {
#             'df': df,
#             'info':  {'response_time': response_time, 'len': len(df)}
#         }
#         return render(response, 'blockchains/pair_balance.html', context=context)
    
#     form = PairFiletrForm() 
#     return render(response, 'blockchains/pair_filter_form.html', {'form': form})

