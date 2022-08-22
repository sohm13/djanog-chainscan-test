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

GROUPBY_FREQ = (
    ('10s', '10s'),
    ('60s', '60s'),
    ('5min', '5min'),
    ('30min', '30minn'),
)







class CompareForm(forms.Form):


    pair = forms.CharField( initial = 'USDT_USDC', required = True)
    blockchains = forms.MultipleChoiceField(choices = BLOCKCHAINS, widget=forms.CheckboxSelectMultiple, initial = BLOCKCHAINS[0])
    dexs = forms.CharField(initial = 'swap', required = True)
    compare_param = forms.ChoiceField( choices = COMPARE_PARAMS)
    groupby_freq = forms.MultipleChoiceField(choices = GROUPBY_FREQ, widget=forms.CheckboxSelectMultiple, initial = GROUPBY_FREQ[0])

    start = forms.DateTimeField(input_formats=["%d-%m-%Y %H:%M"], initial='25-09-2022 20:20')
    end = forms.DateTimeField( input_formats=["%d-%m-%Y %H:%M"], initial = '25-09-2022 20:30')
