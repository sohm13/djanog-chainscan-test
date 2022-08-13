from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from django.core.paginator import Paginator
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

import pandas as pd

from .scripts.events_inspect.blockchain_scan import BlockChainScan
from .scripts.events_inspect.web3_provider import MyWeb3
from .scripts.events_inspect.schemas import Pair


from .models import BSCPair, BscEthSyncEvent, AuroraPair, AuroraEthSyncEvent
from .forms import CompareForm

import time

def index(request):
    return render(request, 'blockchains/index.html')


class BscListView(ListView):
    model = BSCPair
    template_name = 'blockchains/bsc_list.html'
    context_object_name = 'pairs'
    paginate_by = 20

class AuroraListView(ListView):
    model = AuroraPair
    template_name = 'blockchains/aurora_list.html'
    context_object_name = 'pairs'
    paginate_by = 20


def pair_sync_event_to_df(pair: BscEthSyncEvent, decimals_token0: int=18, decimals_token1: int=18):
    pre_to_pandas = [obj.__dict__ for obj in pair ]
    # deep dependency
    timestamps = [p.block_model.timestamp for p in pair]
    symbols = [p.pair_model.pair_symbol for p in pair]

    # print('len(pre_to_pandas)', len(pre_to_pandas))
    # if len(pre_to_pandas) == 0:
    #     return None


    df = pd.DataFrame(pre_to_pandas)
    if len(pre_to_pandas) != 0:
        # df = pd.DataFrame(pre_to_pandas)
        df['timestamp'] = pd.to_datetime(timestamps, unit='s').strftime('%Y-%m-%d %H:%M:%S')

        # print(df.columns)
        df['reserve0'] = df['reserve0'].astype(float) / (10 ** decimals_token0)
        df['reserve1'] = df['reserve1'].astype(float) / (10 ** decimals_token1)
        df['price'] = df['reserve0']/ df['reserve1']
        df['swap0'] = df['reserve0'] - df['reserve0'].shift(-1)
        df['swap1'] = df['reserve1'] - df['reserve1'].shift(-1)
    
    columns_for_desplay = [
        'timestamp',
        'block_number', 
        'transaction_index', 
        'price', 
        # 'pair_address', 
        'reserve0', 
        'reserve1',
        'swap0',
        'swap1',
        'hash'
        ]
    if len(df) > 0:
        return df[columns_for_desplay]
    return pd.DataFrame(columns=columns_for_desplay)


def bsc_pair_detail(request: HttpRequest, pk: int):
    pair_events = BscEthSyncEvent.objects.filter(pair_model=pk).order_by('-id')
    if len(pair_events) == 0:
        return render(request, 'blockchains/not_pair_events.html') 
    pair_model = pair_events[0].pair_model
    pair_df = pair_sync_event_to_df(pair_events, pair_model.token0_decimals, pair_model.token1_decimals)
    
    context = {
        'pair_df': pair_df,
        'ticker': pair_model.pair_symbol,
        'address': pair_model.pair_address,
    }
    
    return render(request, 'blockchains/bsc_detail.html', context=context)

def aurora_pair_detail(request: HttpRequest, pk: int):
    pair_events = AuroraEthSyncEvent.objects.filter(pair_model=pk).order_by('-id')
    if len(pair_events) == 0:
        return render(request, 'blockchains/not_pair_events.html') 
    pair_model = pair_events[0].pair_model
    pair_df = pair_sync_event_to_df(pair_events, pair_model.token0_decimals, pair_model.token1_decimals)
    context = {
        'pair_df': pair_df,
        'ticker': pair_model.pair_symbol,
        'address': pair_model.pair_address,
    }
    
    return render(request, 'blockchains/aurora_detail.html', context=context)





def compare_view(request: HttpRequest):
    context = {}

    if request.method == 'GET':
        context['form']= CompareForm()
        return render(request, 'blockchains/compare_form.html', context)

    form = CompareForm(data=request.POST)
    context['errors'] = form.errors

    if form.is_valid():
        data =  form.cleaned_data
        pairs = BSCPair.objects.filter(pair_symbol=data['pair'])
        print('pairs:', pairs)
        event_pairs = [BscEthSyncEvent.objects.filter(pair_model=pair.pk) for pair in pairs]
        assert len(pairs) == len(event_pairs), "len(pairs) == len(event_pairs) in 'compare_view'"

        df_event_pairs = [pair_sync_event_to_df(event_pairs[i], pairs[i].decimals) for i in range(len(pairs))]

        df_param = [df_event[data['compare_param']].rename(pair.factory_symbol) for df_event, pair in zip(df_event_pairs, pairs)]
        print('df_event_pairs')
        print(df_param)

        df_concat = pd.concat(df_param, axis=1)
        # print(conc)

        context['df'] = df_concat
        context['compare_param'] = data['compare_param']
        # print(df)
        # print('event_pairs', event_pairs[0].__dict__)
        # print(context['form'])
        
    return render(request, 'blockchains/compare_view.html', context)


