from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView

import pandas as pd

from .scripts.events_inpsect.main import get_bsc_chain_scan
from .scripts.events_inpsect.schemas.pair import Pair


from .models import BSCPair, BSCPairTransaction
from .forms import PairFiletrForm

import time

def index(request):
    return render(request, 'blockchains/index.html')


class BscListView(ListView):
    model = BSCPair
    template_name = 'blockchains/bsc_list.html'
    context_object_name = 'transcations'
    paginate_by = 10



class BscDetailView(ListView):
    template_name = 'blockchains/bsc_detail.html'
    context_object_name = 'transaction'

    def get_queryset(self):
        transaction = get_object_or_404(BSCPairTransaction, pk=self.kwargs['pk'])
        return transaction


def pair_balances(response):
    if response.method == 'POST':
        form = PairFiletrForm(response.POST)
        print(type(form), dir(form))
        print(form.data)


        pairs_addresses = form.data['pairs_address'].split(',')
        block_start = int(form.data['block_start'])
        block_end = int(form.data['block_end'])
        pairs = [Pair(address=address, symbol=address) for address in pairs_addresses]
        
        # pairs = [
        #     Pair( address='0x16b9a82891338f9bA80E2D6970FddA79D1eb0daE', symbol='BUSD_WBNB'),
        #     Pair( address='0x8FA59693458289914dB0097F5F366d771B7a7C3F', symbol='MBOX_WBNB'),

        # ]
        # 19395441
        
        tik = time.time()
        bsc = get_bsc_chain_scan()
        transcations = bsc.get_scan_event_from_blocks(block_start, block_end, pairs)
        print('time for resonse',time.time()-tik)


        prices = [int(t.reserve0) / int(t.reserve1) for t in transcations]
        pre_to_pandas = [obj.dict() for obj in transcations ]
        df = pd.DataFrame(pre_to_pandas)
        df['price'] = df['reserve0']/ df['reserve1']
        df = df[['block_number', 'price', 'pair_address']]

  
        context = {
            'transcations': transcations,
            'prices': prices,
            'df': df.to_html(col_space=100)
        }
        return render(response, 'blockchains/pair_balance.html', context=context)
    
    form = PairFiletrForm() 
    return render(response, 'blockchains/pair_filter_form.html', {'form': form})

