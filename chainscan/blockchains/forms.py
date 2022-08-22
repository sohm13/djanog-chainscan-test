from django import forms
# from blockchains.models import NETWORK_MODELS_MAP


COMPARE_PARAMS = (
    ('price', 'PRICE'),
    ('reserve0', 'RESERVE0'),
)

BLOCKCHAINS = (
    ('bsc', 'BSC'),
    ('eth', 'ETH'),
    ('aurora', 'AURORA'),
)



# chains = [ (network, NETWORK_MODELS_MAP[network]['pair_model'].objects.all()) for network in NETWORK_MODELS_MAP.keys()]

dexs = []
# for netowrk, chain in chains:
#     for pair in chain:
#         dexs.append(pair.factory_symbol + f'_{netowrk}')
dexs = set(dexs)
DEXs = [(dex, dex.upper()) for dex in dexs]




class CompareForm(forms.Form):


    pair = forms.CharField( initial = 'USDT_USDC', required = True)
    blockchains = forms.MultipleChoiceField(choices = BLOCKCHAINS, widget=forms.CheckboxSelectMultiple, initial = BLOCKCHAINS[0])
    # dexs = forms.MultipleChoiceField(choices = DEXs, widget=forms.CheckboxSelectMultiple, initial = DEXs[0] if DEXs else '')
    dexs = forms.CharField(initial = 'swap', required = True)
    compare_param = forms.ChoiceField( choices = COMPARE_PARAMS)
    start = forms.DateTimeField(input_formats=["%d-%m-%Y %H:%M"], initial='25-09-2022 20:20')
    end = forms.DateTimeField( input_formats=["%d-%m-%Y %H:%M"], initial = '25-09-2022 20:30')
