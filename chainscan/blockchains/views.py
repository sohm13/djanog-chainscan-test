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


from .models import BSCPair, BscEthSyncEvent
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
        df['token0'] = df['reserve1'] - df['reserve1'].shift(-1)
        df['token1'] = df['reserve0'] - df['reserve0'].shift(-1)
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
