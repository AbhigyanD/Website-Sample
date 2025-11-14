from django import forms


class BranchForm(forms.Form):
    name = forms.CharField(max_length=200, required=True)
    transit_num = forms.CharField(max_length=200, required=True)
    address = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(required=True)
    capacity = forms.IntegerField(required=False, min_value=0)

