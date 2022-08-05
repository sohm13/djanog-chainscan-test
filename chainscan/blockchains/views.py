from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView

import pandas as pd

# from .scripts.events_inpsect.main import get_bsc_chain_scan
# from .scripts.events_inpsect.schemas.pair import Pair


from .models import BSCPair, BSCPairTransaction
from .forms import PairFiletrForm

import time

def index(request):
    return render(request, 'blockchains/index.html')


class BscListView(ListView):
    model = BSCPair
    template_name = 'blockchains/bsc_list.html'
    context_object_name = 'pairs'
    paginate_by = 10



class BscDetailView(ListView):
    template_name = 'blockchains/bsc_detail.html'
    context_object_name = 'transaction'

    def get_queryset(self):
        transaction = get_object_or_404(BSCPairTransaction, pk=self.kwargs['pk'])
        return transaction


def pair_balances(request):
    pass
# def pair_balances(response):
#     if response.method == 'POST':
#         form = PairFiletrForm(response.POST)

#         pairs_addresses = form.data['pairs_address'].split(',')
#         block_start = int(form.data['block_start'])
#         block_end = int(form.data['block_end'])
#         pairs = [Pair(address=address, symbol=address) for address in pairs_addresses]
        
#         tik = time.time()
#         bsc = get_bsc_chain_scan()
#         transcations = bsc.get_scan_event_from_blocks(block_start, block_end, pairs)
#         response_time = time.time()-tik


#         prices = [int(t.reserve0) / int(t.reserve1) for t in transcations]
#         pre_to_pandas = [obj.dict() for obj in transcations ]
#         df = pd.DataFrame(pre_to_pandas)
#         #columns: ['reserve0', 'reserve1', 'hash', 'block_number', 'transaction_index', 'pair_address', 'method'],

#         pair_decimals = 18
#         df['reserve0'] = df['reserve0'] / (10 ** pair_decimals)
#         df['reserve1'] = df['reserve1'] / (10 ** pair_decimals)
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
#             'transcations': transcations,
#             'df': df,
#             'info':  {'response_time': response_time, 'len': len(df)}
#         }
#         return render(response, 'blockchains/pair_balance.html', context=context)
    
#     form = PairFiletrForm() 
#     return render(response, 'blockchains/pair_filter_form.html', {'form': form})

