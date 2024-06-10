from datetime import timedelta
from celery import Celery
from django.utils import timezone
from .models import Produto

app = Celery('app')

@app.task
def desativar_produtos_novos():
    duas_semanas_atras = timezone.now() - timedelta(weeks=2)
    produtos_a_atualizar = Produto.objects.filter(novo=True, data_de_criacao__lte=duas_semanas_atras)
    produtos_a_atualizar.update(novo=False)