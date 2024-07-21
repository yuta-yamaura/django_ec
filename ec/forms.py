from django import forms


class PromtionForm(forms.Form):
    promotion_code = forms.CharField(max_length=7)