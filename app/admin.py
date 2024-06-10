from django.contrib import admin
from .models import *



class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'contato', 'endereco', 'logo', 'rs_facebook', 'rs_instagram', 'rs_tiktok', 'rs_whatsapp', 'meta_titulo', 'meta_descricao', 'palavras_chave']
    
    def has_add_permission(self, request):
        # Verifica se já existem registros no banco de dados para o modelo Empresa
        return Empresa.objects.count() == 0
    

class Ob_vi_miAdmin(admin.ModelAdmin):
    list_display = ['objectivo', 'visao', 'missao', 'termos', 'condicoes', 'pagamento', 'entrega', 'suporte']

    def has_add_permission(self, request):
        # Verifica se já existem registros no banco de dados para o modelo Ob_vi_mi
        return Ob_vi_mi.objects.count() == 0


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'supcat','url']
    search_fields = ['nome']  # Campos pelos quais você deseja fazer a pesquisa
    list_per_page = 15
    raw_id_fields = ('supcat',) 

class MarcaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'url','simblo']
    search_fields = ['nome',]  # Campos pelos quais você deseja fazer a pesquisa
    list_per_page = 15


class ModeloAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']
    list_per_page = 15

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao', 'origem', 'preco', 'promo', 'img', 'marca', 'categ', 'views', 'estado', 'cor', 'data_views', 'data_create', 'status', 'url']
    search_fields = ['nome']
    raw_id_fields = ('marca','categ',)  # Adicione o campo produto ao raw_id_fields

    list_per_page = 10

class proddetimgAdmin(admin.ModelAdmin):
    list_display = ['produto']
    search_fields = ['produto__nome']
    list_per_page = 15
    raw_id_fields = ('produto',)  # Adicione o campo produto ao raw_id_fields


class prodcolorAdmin(admin.ModelAdmin):
    list_display = ['produto']
    search_fields = ['produto__nome']
    list_per_page = 15

class prodpromoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'produto', 'preco', 'desconto']
    search_fields = ['produto__nome']
    list_per_page = 15
    raw_id_fields = ('produto',) 

class SliderAdmin(admin.ModelAdmin):
    list_display = ('pk','activo','img')
    list_per_page = 15
    
class Slider_anuncioAdmin(admin.ModelAdmin):
    list_display = ('pk','activo','img')
    list_per_page = 15

class SuperCategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'url']
    search_fields = ['nome']
    list_per_page = 15


class AgrupamentoAdmin(admin.ModelAdmin):
    list_display = ['pk', 'nome']
    search_fields = ['nome']
    list_per_page = 15
    raw_id_fields = ('supcat',) 

admin.site.register(AgruparSupercateg, AgrupamentoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Marca, MarcaAdmin)
admin.site.register(Modelo, ModeloAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(proddetimg, proddetimgAdmin)
admin.site.register(prodcolor, prodcolorAdmin)
admin.site.register(prodpromo, prodpromoAdmin)
admin.site.register(Slider, SliderAdmin)
admin.site.register(Slider_anuncio, Slider_anuncioAdmin)
admin.site.register(SuperCategoria, SuperCategoriaAdmin)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Ob_vi_mi, Ob_vi_miAdmin)




