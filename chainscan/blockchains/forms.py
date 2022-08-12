from django import forms



COMPARE_PARAMS = (
    ('price', 'PRICE'),
    ('reserve0', 'RESERVE0'),
)

BLOCKCHAINS = (
    ('bsc', 'BSC'),
    ('eth', 'ETH')
)

DEXs = (
    ('pancakeswap', 'PANCAKESWAP'),
    ('biswap', 'BISWAP'),
)



# class DateTimeWidget(forms.widgets.DateTimeInput):

#     def __init__(self, *args, **kwargs):
#         format='%d/%m/%Y %H:%M'
#         attrs={ 
#                 # 'class': 'form-control', 
#                 'placeholder': 'dd-mm-yyyy HH:MM',
#                 'type': 'date',
#                 'size': 100
#                         }

#         super().__init__(format=format, attrs=attrs)


class CompareForm(forms.Form):

    pair = forms.CharField( initial = 'WBNB_USDT', required = True)
    blockchains = forms.MultipleChoiceField(choices = BLOCKCHAINS, widget=forms.CheckboxSelectMultiple, initial = BLOCKCHAINS[0])
    dexs = forms.MultipleChoiceField(choices = DEXs, widget=forms.CheckboxSelectMultiple, initial = DEXs[0])
    compare_param = forms.ChoiceField( choices = COMPARE_PARAMS)
    start = forms.DateTimeField(input_formats=["%d-%m-%Y %H:%M"], initial='25-09-2022 20:20')
    end = forms.DateTimeField( input_formats=["%d-%m-%Y %H:%M"], initial = '25-09-2022 20:30')
