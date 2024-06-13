from django.forms import ModelForm
from .models import OrderdModel
from django.forms.models import formset_factory


class OrderdModelForm(ModelForm):
    class Meta:
        model = OrderdModel
        fields = ('lastname', 'firstname', 'username', 'email', 'address1', 'address2', 'holder', 'credit_card_number', 'date_of_expiry', 'security_code',)

    def save(self, commit=False):
        pass

OrderdModelFormSet = formset_factory(OrderdModelForm)
formset = OrderdModelFormSet()