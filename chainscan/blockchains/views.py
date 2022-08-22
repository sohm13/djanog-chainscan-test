from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from django.core.paginator import Paginator
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

import pandas as pd

from .models import BSCPair, BscEthSyncEvent, AuroraPair, AuroraEthSyncEvent, NETWORK_MODELS_MAP, BSCBlock
from .forms import CompareForm

import time

def pair_sync_event_to_df(pair: BscEthSyncEvent, decimals_token0: int=18, decimals_token1: int=18):
    # print('pair:', pair)
    # tik = time.time()
    pre_to_pandas = [obj.__dict__ for obj in pair ]
    # deep dependency
    timestamps = [p.block_model.timestamp for p in pair]
    # print('*** qs to dict time', time.time() - tik)


    df = pd.DataFrame(pre_to_pandas)
    if len(pre_to_pandas) != 0:
        # df = pd.DataFrame(pre_to_pandas)
        df['timestamp'] = pd.to_datetime(timestamps, unit='s')#.strftime('%Y-%m-%d %H:%M:%S')

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
        'pair_address', 
        'reserve0', 
        'reserve1',
        'swap0',
        'swap1',
        'hash'
        ]
    if len(df) > 0:
        return df[columns_for_desplay]
    return pd.DataFrame(columns=columns_for_desplay)








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


def bsc_pair_detail(request: HttpRequest, pk: int=None, pair_symbol: str = None):
    tik = time.time()
    pair_events = []
    event_model = BscEthSyncEvent
    if pk:
        pair_events = event_model.objects.filter(pair_model=pk).order_by('-block_number').select_related('block_model')
    if pair_symbol:
        pair_events = event_model.objects.filter(pair_model__pair_symbol=pair_symbol).order_by('-block_number').select_related('block_model')

    if len(pair_events) == 0:
        return render(request, 'blockchains/not_pair_events.html') 
    pair_model = pair_events[0].pair_model
    pair_df = pair_sync_event_to_df(pair_events, pair_model.token0_decimals, pair_model.token1_decimals)
    
    context = {
        'pair_df': pair_df,
        'ticker': pair_model.pair_symbol,
        'address':pair_df['pair_address'].unique() #pair_model.pair_address,
    }
    print('***time bsc pair detail:', time.time() - tik)
    
    return render(request, 'blockchains/bsc_detail.html', context=context)

def aurora_pair_detail(request: HttpRequest, pk: int=None, pair_symbol: str = None):
    pair_events = []
    event_model = AuroraEthSyncEvent
    print('request', request)
    if pk:
        pair_events = event_model.objects.filter(pair_model=pk).order_by('-block_number').select_related('block_model')
    if pair_symbol:
        pair_events = event_model.objects.filter(pair_model__pair_symbol=pair_symbol).order_by('-block_number').select_related('block_model')

    # pair_events = AuroraEthSyncEvent.objects.filter(pair_model=pk).order_by('-id').select_related('block_model')
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

        chains = [ (network, NETWORK_MODELS_MAP[network]['pair_model'].objects.all()) for network in NETWORK_MODELS_MAP.keys()]

        dexs = []
        for netowrk, chain in chains:
            for pair in chain:
                dexs.append(pair.factory_symbol + f'_{netowrk}')
        dexs = set(dexs)
        DEXs = [(dex, dex.upper()) for dex in dexs]

        data = {'dexs': list(dexs) }
        form = CompareForm(initial=data)
        context['form']= form
        return render(request, 'blockchains/compare_form.html', context)

    form = CompareForm(data=request.POST)
    context['errors'] = form.errors

    if form.is_valid():
        data =  form.cleaned_data
        group_freq = data['groupby_freq'][0]
        chains = [ (network, NETWORK_MODELS_MAP[network]) for network in NETWORK_MODELS_MAP.keys() if network in data['blockchains'] ]
       
        df_chains_param = []
        for network_name, chain in chains:
            pairs = chain['pair_model'].objects.filter(pair_symbol=data['pair'])
            tik = time.time()
            event_pairs = [chain['eth_sync_event_model'].objects.filter(pair_model=pair.pk).select_related('block_model') for pair in pairs]
            assert len(pairs) == len(event_pairs), "len(pairs) == len(event_pairs) in 'compare_view'"
            print('**event_pairs',  sum([len(p) for p in event_pairs]), 'time', time.time() - tik)

            tik = time.time()
            df_event_pairs = [pair_sync_event_to_df(event_pairs[i], pairs[i].decimals) for i in range(len(pairs))]
            print('**df_event_pairs time:', time.time() - tik)

            tik = time.time()
            df_param = []
            for df_event, pair in zip(df_event_pairs, pairs):
                if len(df_event) == 0:
                    continue
                # print('df_event', df_event)
                _data_add = df_event[[data['compare_param'], 'timestamp']] 
                # _data_add.rename(columns={data['compare_param']: pair.factory_symbol, 'timestamp': f'timestamp_{pair.factory_symbol}'}, inplace=True)
                _data_add = _data_add.rename(columns={data['compare_param']: pair.factory_symbol})
                _df_grp = _data_add.groupby(pd.Grouper(key='timestamp', freq=group_freq )).last()
                df_param.append(_df_grp)
                print('!',pair.factory_symbol, len(_data_add), len(_df_grp))
            df_chains_param.extend(df_param)
            print('**make df time:', time.time()-tik)

        if len(df_chains_param)  == 0:
            return render(request, 'blockchains/not_pair_events.html')
        df_concat =  pd.concat(df_chains_param, axis=1)
        df_concat['time'] = df_concat.index.astype('str')
    
        # print(df_concat.head())

        context['df'] = df_concat.iloc[::-1]
        context['compare_param'] = data['compare_param']
        
    return render(request, 'blockchains/compare_view.html', context)


