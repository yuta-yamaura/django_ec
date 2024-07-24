from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
import random
from ec.models import PromotionCodeModel

class Command(BaseCommand):
    help = "プロモーションコード生成コマンド"

    def handle(self, *args, **options):
        for n in range(10):
            code = get_random_string(7)
            amount = random.randint(100, 1000)
            
            obj, created = PromotionCodeModel.objects.get_or_create(
                code = code,
                amount = amount
            )