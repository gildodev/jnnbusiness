from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
import hashlib,uuid
from ckeditor.fields import RichTextField 
from django.urls import reverse

import ckeditor



class Empresa(models.Model):
    nome = models.CharField(max_length=100)
    slogan = models.CharField(max_length=500, default='O Meu Grande Amigo')
    email = models.EmailField(max_length=100)
    contato = models.CharField(max_length=100)
    endereco = models.TextField()
    logo = models.ImageField(upload_to='imagens_empresa/', blank=True)
    erro404 = models.ImageField(upload_to='imagens_erro/', null=True, blank=True)
    rs_facebook = models.URLField(max_length=200, null=True, blank=True)
    rs_instagram = models.URLField(max_length=200, null=True, blank=True)
    rs_tiktok = models.URLField(max_length=200, null=True, blank=True)
    rs_whatsapp = models.CharField(max_length=15, null=True, blank=True, default='+258')

    # Informações de SEO
    meta_titulo = models.CharField(max_length=100, help_text='Título de SEO da Empresa')
    meta_descricao = models.TextField(help_text='Descrição de SEO da Empresa')
    palavras_chave = models.CharField(max_length=100, help_text='Palavras-chave de SEO separadas por vírgulas')
    
    def __str__(self):
        return self.nome
    
class Ob_vi_mi(models.Model):
    objectivo = models.TextField(max_length=500)
    visao = models.TextField(max_length=500)
    missao = models.TextField(max_length=500)
    termos = models.TextField(max_length=500)
    condicoes = models.TextField(max_length=500)
    pagamento = models.CharField(max_length=500,help_text='Descreva a forma de pagamento')
    entrega = models.CharField(max_length=500,help_text='Descreva a forma de entrega')
    suporte = models.CharField(max_length=500,help_text='Descreva a forma de atendimento ao cliente')
    
    def __str__(self):
        return self.objectivo


class SuperCategoria(models.Model):
    nome=models.CharField(max_length=100, unique=True)
    url=models.SlugField(unique=True,editable=False)
    num_categ=models.IntegerField(default=0, editable=True)
    activo=models.BooleanField(default=True)

    def actualizarCateg(self):
        self.num_categ=self.categoria_set.count()
        return self.num_categ

    def save(self, *args,**kwargs):
        url=str(self.nome)

        self.url=slugify(url)
        super(SuperCategoria,self).save(*args,**kwargs)

    def __str__(self):
        return self.nome

class AgruparSupercateg(models.Model):
    supcat=models.ForeignKey(SuperCategoria,on_delete=models.CASCADE)
    nome=models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class Categoria(models.Model):
    supcat=models.ForeignKey(SuperCategoria,null=True ,on_delete=models.CASCADE)
    agrupamento=models.ForeignKey(AgruparSupercateg,on_delete=models.CASCADE)
    nome=models.CharField(max_length=100, unique=True)
    url=models.SlugField(unique=True,editable=False)
    activo=models.BooleanField(default=True)

    def save(self, *args,**kwargs):
        url=str(self.nome).lower()
        self.url=slugify(url)
        super(Categoria,self).save(*args,**kwargs)
        self.supcat.actualizarCateg()

    def __str__(self):
        return self.nome

class Marca(models.Model):
    nome=models.CharField(max_length=100, unique=True)
    simblo = models.ImageField(upload_to='imagens_marca/', null=True, blank=True)
    url=models.SlugField(unique=True,editable=False)

    def save(self, *args,**kwargs):
        url=str(self.nome).lower()
        self.url=slugify(url)
        super(Marca,self).save(*args,**kwargs)

    def __str__(self):
        return self.nome

class Modelo(models.Model):
    nome=models.CharField(max_length=100, unique=True)
    url=models.SlugField(unique=True,editable=False)

    def save(self, *args,**kwargs):
        url=str(self.nome).lower()
        self.url=slugify(url)
        super(Modelo,self).save(*args,**kwargs)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome =models.CharField(max_length=100,)
    descricao = RichTextField()
    origem = models.CharField(max_length=100,null=True)
    preco = models.DecimalField(max_digits=65, decimal_places=2)
    promo = models.DecimalField(max_digits=65, decimal_places=2, default=0.00, editable=False)
    img = models.ImageField(upload_to='imagens_produto/', blank=True)
    marca=models.ForeignKey(Marca, null=True ,on_delete=models.CASCADE)
    categ=models.ForeignKey(Categoria, on_delete=models.CASCADE)
    views=models.BigIntegerField(default=0, editable=False)
    estado=models.CharField(max_length=100,default='Novo', choices=(('Novo','Novo'),('Novo mais usado','Novo mais usado'),('Usado','Usado')))
    cor = models.CharField(max_length=100, default='Branco')
    data_views=models.DateField(auto_now_add=False, null=True, editable=False)
    data_create=models.DateField(auto_now_add=True)
    novo=models.BooleanField(default=True, editable=False)
    status=models.CharField(max_length=100,default='Activo', choices=(('Activo','Activo'),('Inactivo','Inactivo')))
    url=models.SlugField(unique=True,editable=False)

    def save(self, *args, **kwargs):
        # Gere a URL com base no nome
        base_url = str(self.nome).lower()
        base_url = slugify(base_url)
        
        # Verifique se uma URL com base_url já existe no banco de dados
        existem_urls_similares = Produto.objects.filter(url__startswith=base_url).exists()

        if existem_urls_similares:
            # Se existirem URLs similares, use uuid para evitar duplicatas
            sufixo = "shop"
            self.url = f"{base_url}-{sufixo}"
        else:
            self.url = base_url

        pd = Produto.objects.get(pk=self.pk)
        if self.preco < pd.preco:
            self.promo = pd.preco
            

        super(Produto, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.nome
    
    def get_absolute_url(self):
        return f'/produto/{self.url}'

class proddetimg(models.Model):
    produto=models.OneToOneField(Produto, on_delete=models.CASCADE)
    det_img1 = models.ImageField(upload_to='imagens_produto/', blank=True)
    det_img2 = models.ImageField(upload_to='imagens_produto/', blank=True, null=True)
    det_img3 = models.ImageField(upload_to='imagens_produto/', blank=True, null=True)
    det_img4 = models.ImageField(upload_to='imagens_produto/', blank=True, null=True)

    def __str__(self):
        return self.produto.nome


class prodsize(models.Model):
    produto=models.OneToOneField(Produto, on_delete=models.CASCADE)
    nome=models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class prodcolor(models.Model):
    produto=models.OneToOneField(Produto, on_delete=models.CASCADE)
    det_color1 = models.ImageField(upload_to='imagens_produto/', blank=True, null=True)
    det_color2 = models.ImageField(upload_to='imagens_produto/', blank=True, null=True)
    det_color3 = models.ImageField(upload_to='imagens_produto/', blank=True, null=True)
    det_color4 = models.ImageField(upload_to='imagens_produto/', blank=True, null=True)

    def __str__(self):
        return self.produto.nome


class prodpromo(models.Model):
    produto=models.OneToOneField(Produto, on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=60, decimal_places=2)
    desconto = models.DecimalField(max_digits=60, decimal_places=2, editable=False)
    data_inicio = models.DateTimeField(auto_now_add=False)
    data_fim= models.DateTimeField(auto_now_add=False)
    status=models.CharField(max_length=100,default='Activo', choices=(('Activo','Activo'),('Inactivo','Inactivo')))

    @property
    def promo_atual(self):
        return self.produto.preco
    
    @property
    def nome(self):
        return self.produto.nome
    

    def __str__(self):
        return str(self.preco)
    
    def save(self, *args, **kwargs):
        # Verifica se o preço da promoção é menor que o preço do produto
        if self.preco >= self.produto.preco:
            raise ValueError("O preço da promoção deve ser menor que o preço do produto.")
        else:
            self.desconto = (1-(self.preco / self.produto.preco)) * 100

        super(prodpromo, self).save(*args, **kwargs)

class Slider(models.Model):
    nome=RichTextField(blank=True)
    descricao = RichTextField(blank=True)
    nome_mobile =RichTextField(blank=True)
    descricao_mobile = RichTextField(blank=True)
    img = models.ImageField(upload_to='imagens_slide/', blank=True)
    activar_texto=models.BooleanField(default=True)
    activo=models.BooleanField(default=True)
    
    def __str__(self):
        return self.nome

class Slider_anuncio(models.Model):
    img = models.ImageField(upload_to='imagens_anuncio/', blank=True)
    activo=models.BooleanField(default=True)

    def __str__(self):
        return f'{self.pk}'
    

