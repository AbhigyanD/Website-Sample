from django import forms


class BankForm(forms.Form):
    name = forms.CharField(max_length=200, required=True)
    description = forms.CharField(max_length=200, required=True)
    inst_num = forms.CharField(max_length=200, required=True)
    swift_code = forms.CharField(max_length=200, required=True)

