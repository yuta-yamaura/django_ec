from django import forms


class PromtionForm(forms.Form):
    code = forms.CharField(max_length=7)