from django.conf import settings
from ec.models import ProductModel

def base(request):
    items = ProductModel.objects.order_by('created_at').reverse()
    return {
        'RECENT_ITEMS' : items
    }