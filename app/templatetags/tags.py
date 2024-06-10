from django import template
from app.models import Empresa
register = template.Library()

conf=Empresa.objects.first()

@register.simple_tag
def logotipo():
    return conf.logo.url

@register.simple_tag
def erro():
    return conf.erro404.url


@register.simple_tag
def titulo():
    return conf.nome