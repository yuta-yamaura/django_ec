from django import forms
from .models import OrderdModel


class PostForm(forms.ModelForm):
    class Meta:
        model = OrderdModel
        fields = ('lastname', 'firstname', 'username', 'email', 'address1', 'address2', 'holder',  'credit_card_number', 'date_of_expiry', 'security_code')