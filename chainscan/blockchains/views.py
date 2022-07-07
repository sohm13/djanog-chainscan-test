from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


from .models import BSCTransaction



def index(request):
    return render(request, 'blockchains/index.html')


class BscListView(ListView):
    model = BSCTransaction
    template_name = 'blockchains/bsc_list.html'
    context_object_name = 'transcations'
    paginate_by = 2



class BscDetailView(ListView):
    template_name = 'blockchains/bsc_detail.html'
    context_object_name = 'transaction'

    def get_queryset(self):
        transaction = get_object_or_404(BSCTransaction, pk=self.kwargs['pk'])
        return transaction