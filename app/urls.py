from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.views.defaults import permission_denied
from django.views.defaults import page_not_found
from django.contrib.sitemaps.views import sitemap
from .sitemaps import ProdutoSitemap
from django.contrib.sitemaps import GenericSitemap  # new
from django.contrib.sitemaps.views import sitemap  # new

sitemaps = {
    'produtos': ProdutoSitemap,
}

handler404 = erro_404
handler403 = permission_denied

urlpatterns = [
    # Suas outras rotas
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('',app.index, name='home'),
    path('produto/<slug:prod>/', produto.produto, name='prod'),
    path('catologo/<slug:sp>/', catologo.catologo, name='sp'),
    path('catologo/page/<slug:sp>/', catologo.catologo_page, name='sp_page'),
    path('categoria/<slug:cat>/', catologo.categoria, name='cat'),
    path('categoria/page/<slug:cat>', catologo.categoria_page, name='cat_page'),
    path('pesquisar/', produto.pesquisa, name='pesq'),
    path('page/pesquisar/', produto.pesquisa_page, name='pesq_page'),
    path('api-lista-prod-index/', api.list_prod_index, name='api_prod_index'),
    path('api-lista-prod/', api.list_prod, name='api_prod'),
    path('api-menor-maior-preco-prod/', api.precoprod, name='api_mmp'),
    path('api-ordery-prod/', api.catologo_ordery, name='api_ordery'),
    
]

# Configuração para servir arquivos estáticos durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
