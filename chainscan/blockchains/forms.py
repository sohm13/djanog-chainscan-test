from django import forms


class PairFiletrForm(forms.Form):

    pairs_address = forms.CharField()
    block_chain = forms.CharField(max_length=10)
    block_start = forms.IntegerField()
    block_end = forms.IntegerField()
