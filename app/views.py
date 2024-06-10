from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from django.contrib.auth.decorators import login_required
from geopy.geocoders import Nominatim
from django.db.models import Min, Max
from .models import *
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from ipware import get_client_ip
import geocoder
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import datetime
from django.db.models import Q
from django.shortcuts import get_object_or_404
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Count
from django.db.models import F, FloatField, ExpressionWrapper
from django.views.generic import DetailView



# Create your views here.

# Class de pagina inicial

class app:
    # @login_required(login_url='auth/login')
    def index(request):
        config_site = Empresa.objects.first()
        config_tarefa = Ob_vi_mi.objects.first()
        slider=Slider.objects.all().exclude(activo=False)
        slider_an=Slider_anuncio.objects.all().exclude(activo=False)
        spcateg=SuperCategoria.objects.all().exclude(activo=False)
        categ=Categoria.objects.all().exclude(activo=False)
        prod=Produto.objects.all().exclude(status='Inactivo')
        promo=prodpromo.objects.all()
        data_atual = datetime.now()
        prod_novo=Produto.objects.filter(data_create__month=data_atual.month,data_create__year=data_atual.year).exclude(status='Inactivo').order_by('-pk')
        achados=prod.order_by('-data_views').exclude(status='Inactivo')[:12]

        lista=[]
        for pd in prod:
            if pd.promo > 0:
                lista.append({
                    'pk':pd.pk,
                    'desconto':((pd.preco - pd.promo) / pd.preco)*100
                })

        return render(request,'index.html',{'achados':achados,'promo':promo,'desconto':lista,'novo_prod':prod_novo,'tarefa':config_tarefa,'conf':config_site,'anuncio':slider_an,'slider':slider,'prod':prod,'categ':categ,'spcateg':spcateg})


class api:

    def precoprod(request):
        menor_preco = Produto.objects.aggregate(Min('preco'))['preco__min']
        maior_preco = Produto.objects.aggregate(Max('preco'))['preco__max']
        dados=[{'menor':menor_preco,'maior':maior_preco}]
        return JsonResponse({'data':dados})


    def list_prod_index(request):
        pagina = request.GET.get('pg')
        prod=Produto.objects.all().exclude(status='Inactivo').order_by('-views')
        html=""
        paginator = Paginator(prod, 18)
        produtos=paginator.get_page(pagina)
        if  paginator.num_pages < 18:
            html += f'''
            <script>
                var buttons = document.querySelector(".btn-vermais");
                buttons.classList.add('d-none');
            </script>
            '''
        
        dados=[]
        for prod in produtos:
            html += f'''
        <div class="col-md-2 col-4 mb-2">
            <div class="produto-content">
                <small class="text-muted"><i class="fa fa-tags"></i> {prod.categ}</small>
                <div class="produto-img">
                    <a href="/produto/{prod.url}" class="produto-titulo"><img src="{prod.img.url}" alt=""></a>
                </div>
                <div class="produto-detalhe mb-2">
                    <a href/produto/{prod.url}" class="produto-titulo">{prod}</a>
                </div>
                <div class="produto-precos">
                    {'<del class="prod-promo">{}</del>'.format(prod.promo) if prod.promo and prod.promo > prod.preco else ''}
                    <span class="prod-preco">{prod.preco}</span>
                </div>
            </div>
        </div>
        '''

        return HttpResponse(html, content_type='text/html')
    
    def list_prod(request):
        pagina = request.GET.get('pg')
        prod=Produto.objects.all().exclude(status='Inactivo').order_by('-views')
        
        paginator = Paginator(prod, 18)
        produtos=paginator.get_page(pagina)
        html=""
        if paginator.num_pages == int(pagina):
            html += f'''
            <script>
                var buttons = document.querySelector(".btn-vermais");
                buttons.classList.add('d-none');
            </script>
            '''
        
        dados=[]
        for prod in produtos:
            html += f'''
        <div class="col-md-2 col-4 mb-2">
            <div class="produto-content">
                <small class="text-muted"><i class="fa fa-tags"></i> {prod.categ}</small>
                <div class="produto-img">
                    <a href="/produto/{prod.url}" class="produto-titulo"><img src="{prod.img.url}" alt=""></a>
                </div>
                <div class="produto-detalhe mb-2">
                    <a href/produto/{prod.url}" class="produto-titulo">{prod}</a>
                </div>
                <div class="produto-precos">
                    {'<del class="prod-promo">{}</del>'.format(prod.promo) if prod.promo and prod.promo > prod.preco else ''}
                    <span class="prod-preco">{prod.preco}</span>
                </div>
            </div>
        </div>
        '''
        
        return HttpResponse(html, content_type='text/html')
    


    def catologo_ordery(request,sp):
        page=request.GET.get('page')
        ordery=request.GET.get('ordery')
        if not ordery:
            ordery='-views'
        config_site = Empresa.objects.first()
        config_tarefa = Ob_vi_mi.objects.first()
        sp=SuperCategoria.objects.get(url=sp)
        sps=SuperCategoria.objects.all().exclude(pk=sp.pk)
        cat=Categoria.objects.filter(supcat=sp)
        
        marca=Marca.objects.all()
        cor=prodcolor.objects.all()
        # Coleta todos os produtos de todas as categorias
        all_products = []
        prod=[]
        total=0
        for cats in cat:
            cats = Categoria.objects.get(pk=cats.pk)
            pd = Produto.objects.filter(categ=cats, status='activo').order_by(ordery)
            all_products.extend(pd)
            total +=1
        
        num_itens = 12
        paginator = Paginator(all_products, num_itens)  # Pagina 2 produtos por página

        pds = paginator.get_page(page)
        count = paginator.get_page
        for pd in pds:
            prod.append({
                'pk': pd.pk,
                'nome':pd.nome,
                'preco':pd.preco,
                'promo':pd.promo,
                'img':pd.img,
                'url':pd.url,
                'cat':pd.categ,
                'cat_url':pd.categ.url,
                'desc':pd.descricao,
                'made':pd.origem,
                
            })

        return render(request,'catologo/catologo.html',{'sps':sps,'count':count,'page':pds,'prod':prod,'marca':marca,'cor':cor,'sp':sp,'cat':cat,'tarefa':config_tarefa,'conf':config_site,})
    
class catologo:

    def catologo_page(request,sp):
        page=request.GET.get('page')
        ordery=request.GET.get('ordery')
        marc=request.GET.get('marc')
        if not ordery:
            ordery='-views'
        config_site = Empresa.objects.first()
        config_tarefa = Ob_vi_mi.objects.first()
        sp=SuperCategoria.objects.get(url=sp)
        cat=Categoria.objects.filter(supcat=sp)
        sps=SuperCategoria.objects.all().exclude(pk=sp.pk)
        marca=Marca.objects.all()
        cor=prodcolor.objects.all()
        # Coleta todos os produtos de todas as categorias
        all_products = []
        prod=[]
        total=0
        mc=marc
        for cats in cat:
            if marc:
                mc=Marca.objects.get(nome=marc)
                pd = Produto.objects.filter(categ=cats, marca=mc,status='activo').order_by(ordery)
            else:
                cats = Categoria.objects.get(pk=cats.pk)
                pd = Produto.objects.filter(categ=cats, status='activo').order_by(ordery)

            all_products.extend(pd)
        
        num_itens = 12
        paginator = Paginator(all_products, num_itens)  # Pagina 2 produtos por página

        pds = paginator.get_page(page)
        count = paginator.get_page
        for pd in pds:
            prod.append({
                'pk': pd.pk,
                'nome':pd.nome,
                'preco':pd.preco,
                'promo':pd.promo,
                'img':pd.img,
                'url':pd.url,
                'cat':pd.categ,
                'cat_url':pd.categ.url,
                'desc':pd.descricao,
                'made':pd.origem,
            })
        sup=SuperCategoria.objects.all()
        categ=Categoria.objects.all()
        return render(request,'catologo/catologo.html',{'spcateg':sup,'sps':sps,'categ':categ,'count':ordery,'page':pds,'prod':prod,'marca':marca,'marc':mc,'cor':cor,'sp':sp,'cat':cat,'tarefa':config_tarefa,'conf':config_site,})



    def catologo(request,sp):
        config_site = Empresa.objects.first()
        config_tarefa = Ob_vi_mi.objects.first()
        sp=SuperCategoria.objects.get(url=sp)
        cat=Categoria.objects.filter(supcat=sp)
        sps=SuperCategoria.objects.all().exclude(pk=sp.pk)
        marca=Marca.objects.all()
        cor=prodcolor.objects.all()
        # Coleta todos os produtos de todas as categorias
        all_products = []
        prod=[]
        for cats in cat:
            cats = Categoria.objects.get(pk=cats.pk)
            pd = Produto.objects.filter(categ=cats, status='activo').order_by('-views')
            all_products.extend(pd)

        page = 1
        num_page = 12
        inicio = (page - 1) * num_page
        fim = inicio + num_page
        paginator = Paginator(all_products, num_page)  # Pagina 2 produtos por página

        pds = paginator.get_page(page)
        count = paginator.get_page
        for pd in pds:
            prod.append({
                'pk': pd.pk,
                'nome':pd.nome,
                'preco':pd.preco,
                'promo':pd.promo,
                'img':pd.img,
                'url':pd.url,
                'cat':pd.categ,
                'cat_url':pd.categ.url,
                'desc':pd.descricao,
                'made':pd.origem,
            })

        if request.method == 'POST':
            pass
        sup=SuperCategoria.objects.all()
        categ=Categoria.objects.all().exclude(supcat=sp)
        return render(request,'catologo/catologo.html',{'categ':categ, 'sps':sps,'spcateg':sup,'count':count,'page':pds,'prod':prod,'marca':marca,'cor':cor,'sp':sp,'cat':cat,'tarefa':config_tarefa,'conf':config_site,})


    def categoria_page(request,cat):
        page=request.GET.get('page')
        ordery=request.GET.get('ordery')
        marc=request.GET.get('marca')
        if not ordery:
            ordery='-views'
        config_site = Empresa.objects.first()
        config_tarefa = Ob_vi_mi.objects.first()
        cat=Categoria.objects.get(url=cat)
        sp=cat.supcat
        cats=Categoria.objects.filter(supcat=sp).exclude(pk=cat.pk)
        marca=Marca.objects.all()
        cor=prodcolor.objects.all()
        # Coleta todos os produtos de todas as categorias
        all_products = []
        prod=[]
        mar=marc

        if marc:
            mar=Marca.objects.get(nome=marc)
            pd = Produto.objects.filter(categ=cat,marca=mar ,status='activo').order_by(ordery)
        else:
            pd = Produto.objects.filter(categ=cat, status='activo').order_by(ordery)
        all_products.extend(pd)

        page = 1
        num_page = 12
        inicio = (page - 1) * num_page
        fim = inicio + num_page
        paginator = Paginator(all_products, num_page)  # Pagina 2 produtos por página

        pds = paginator.get_page(page)
        count = paginator.get_page
        for pd in pds:
            prod.append({
                'pk': pd.pk,
                'nome':pd.nome,
                'preco':pd.preco,
                'promo':pd.promo,
                'img':pd.img,
                'url':pd.url,
                'cat':pd.categ,
                'cat_url':pd.categ.url,
                'desc':pd.descricao,
                'made':pd.origem,
            })

        if request.method == 'POST':
            pass
        sup=SuperCategoria.objects.all()
        categ=Categoria.objects.all().exclude(supcat=sp)
        return render(request,'catologo/categoria.html',{'spcateg':sup,'categ':categ,'categs':cat,'count':count,'count':ordery,'page':pds,'prod':prod,'marca':marca,'marc':mar,'cor':cor,'sp':cat.supcat,'cat':cats,'tarefa':config_tarefa,'conf':config_site,})


    def categoria(request,cat):
        config_site = Empresa.objects.first()
        config_tarefa = Ob_vi_mi.objects.first()
        categ=Categoria.objects.get(url=cat)
        sp=categ.supcat
        cats=Categoria.objects.filter(supcat=sp).exclude(pk=categ.pk)
        marca=Marca.objects.all()
        cor=prodcolor.objects.all()
        # Coleta todos os produtos de todas as categorias
        all_products = []
        prod=[]
        pd = Produto.objects.filter(categ=categ, status='activo').order_by('-views')
        all_products.extend(pd)

        page = 1
        num_page = 12
        inicio = (page - 1) * num_page
        fim = inicio + num_page
        paginator = Paginator(all_products, num_page)  # Pagina 2 produtos por página

        pds = paginator.get_page(page)
        count = paginator.get_page
        for pd in pds:
            prod.append({
                'pk': pd.pk,
                'nome':pd.nome,
                'preco':pd.preco,
                'promo':pd.promo,
                'img':pd.img,
                'url':pd.url,
                'cat':pd.categ,
                'cat_url':pd.categ.url,
                'desc':pd.descricao,
                'made':pd.origem,
            })

        if request.method == 'POST':
            pass
        sup=SuperCategoria.objects.all()
        categs=Categoria.objects.all().exclude(supcat=sp)
        return render(request,'catologo/categoria.html',{'spcateg':sup,'categ':categs,'categs':categ,'count':count,'page':pds,'prod':prod,'marca':marca,'cor':cor,'sp':categ.supcat,'cat':cats,'tarefa':config_tarefa,'conf':config_site,})

class DetalhesProdutoView(DetailView):
    model = Produto
    template_name = 'produto-detalhes.html'
    context_object_name = 'produto'

class produto:

    def produto(request,prod):
        from datetime import datetime
        config_site = Empresa.objects.first()
        config_tarefa = Ob_vi_mi.objects.first()
        # Use get_object_or_404 para recuperar um único objeto com base na URL
        prod_cat=None
        produto = Produto.objects.filter(url=prod).first()
        q=produto.nome;

        prod_cat=Produto.objects.filter( status='activo').order_by('-views').exclude(pk=produto.pk)

        promo=[]
        if produto and prodpromo.objects.filter(produto=produto).exists():
            promo=prodpromo.objects.filter(produto=produto).first()

        # produto=[pd for pd in produto]
        detimg= []
        if produto and proddetimg.objects.filter(produto=produto).exists():
            detimg= proddetimg.objects.filter(produto=produto).first()
            

        prods=Produto.objects.filter(url__startswith=prod).first()
        if prods:
            prods.views+=1
            prods.data_views=datetime.now()
            prods.save()
        spcateg=SuperCategoria.objects.all()
        categ=Categoria.objects.all()

        
        return render(request,'catologo/produto.html',{'categ':categ,'spcateg':spcateg,'promo':promo,'prod_cat':prod_cat,'prod':produto,'detimg':detimg,'tarefa':config_tarefa,'conf':config_site,})


    def pesquisa(request):
        config_site = Empresa.objects.first()
        config_tarefa = Ob_vi_mi.objects.first()
        categ = request.GET.get('categoria')
        q = request.GET.get('q')
        catpk=categ
        # Inicialmente, obtenha todos os produtos
        
        prod = Produto.objects.filter(Q(nome__icontains=q)|Q(descricao__icontains=q)).exclude(status='inactivo')
        produtos = Produto.objects.all().order_by('-views').exclude(pk__in=prod.values_list('pk', flat=True))
        categs=[]
        # Verifique se a categoria foi fornecida e filtre os produtos por categoria
        
        
        if q:
            # Pré-processamento dos dados e criação de vetores TF-IDF
            tfidf_vectorizer = TfidfVectorizer()
            corpus = [produto.nome + ' ' + produto.descricao for produto in produtos]
            tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

            # Vetorize o termo de pesquisa
            query_vector = tfidf_vectorizer.transform([q])

            # Calcule a similaridade do cosseno entre o termo de pesquisa e todos os produtos
            cosine_similarities = cosine_similarity(query_vector, tfidf_matrix)

            # Obtém os índices dos produtos ordenados por similaridade do cosseno
            similaridade_indices = cosine_similarities[0].argsort()[::-1]

            # Converta os índices para inteiros de 32 bits (int32)
            similaridade_indices = similaridade_indices.astype('int32')

            # Ordene os produtos com base na similaridade do cosseno
            produtos = [produtos[int(i)] for i in similaridade_indices]
            page = 1
            num_page = 24
            inicio = (page - 1) * num_page
            fim = inicio + num_page
            paginator = Paginator(prod, num_page)  # Pagina 2 produtos por página

            prod = paginator.get_page(page)
            
            count = paginator.get_page
            categ = Categoria.objects.all()
            spcateg=SuperCategoria.objects.all()
        
        return render(request,'catologo/pesquisa.html',{'spcateg':spcateg,'catpk':catpk,'categ':categ,'count':count,'rel':produtos,'produtos':prod,'q':q,'tarefa':config_tarefa,'conf':config_site,})



    def pesquisa_page(request):
        config_site = Empresa.objects.first()
        config_tarefa = Ob_vi_mi.objects.first()
        categ = request.GET.get('categoria')
        q = request.GET.get('q')
        page = request.GET.get('page')
        catpk=categ
        # Inicialmente, obtenha todos os produtos
        prod = Produto.objects.filter(Q(nome__icontains=q)|Q(descricao__icontains=q)).exclude(status='inactivo')
        produtos = Produto.objects.all().order_by('-views').exclude(pk__in=prod.values_list('pk', flat=True))
        categs=[]
        spcateg=SuperCategoria.objects.all()
        # Verifique se a categoria foi fornecida e filtre os produtos por categoria
        if categ:
            categoria = Categoria.objects.get(pk=categ)
            produtos = produtos.filter(categ=categoria)
            categs = produtos.filter(categ=categoria)
            prod = Produto.objects.filter(Q(nome__icontains=q)|Q(descricao__icontains=q) & Q(categ=categoria)).exclude(status='inactivo')
            
        
        if q:
            # Pré-processamento dos dados e criação de vetores TF-IDF
            tfidf_vectorizer = TfidfVectorizer()
            corpus = [produto.nome + ' ' + produto.descricao for produto in produtos]
            tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

            # Vetorize o termo de pesquisa
            query_vector = tfidf_vectorizer.transform([q])

            # Calcule a similaridade do cosseno entre o termo de pesquisa e todos os produtos
            cosine_similarities = cosine_similarity(query_vector, tfidf_matrix)

            # Obtém os índices dos produtos ordenados por similaridade do cosseno
            similaridade_indices = cosine_similarities[0].argsort()[::-1]

            # Converta os índices para inteiros de 32 bits (int32)
            similaridade_indices = similaridade_indices.astype('int32')

            # Ordene os produtos com base na similaridade do cosseno
            produtos = [produtos[int(i)] for i in similaridade_indices]
           
            num_page = 24
            paginator = Paginator(prod, num_page)  # Pagina 2 produtos por página

            prod = paginator.get_page(page)
            
            count = paginator.get_page
            categ = Categoria.objects.all()
        
        return render(request,'catologo/pesquisa.html',{'spcateg':spcateg, 'catpk':catpk,'categ':categ,'count':count,'rel':produtos,'produtos':prod,'q':q,'tarefa':config_tarefa,'conf':config_site,})

def erro_404(request, exception):
    return render(request, '404.html', status=404)