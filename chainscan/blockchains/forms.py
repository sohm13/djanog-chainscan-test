from django import forms


class PairFiletrForm(forms.Form):

    pairs_address = forms.CharField( initial = '0x16b9a82891338f9bA80E2D6970FddA79D1eb0daE')
    block_chain = forms.CharField(max_length=10, initial = 'bsc')
    block_start = forms.IntegerField(initial = 19395441)
    block_end = forms.IntegerField(initial = 19395441+10)
