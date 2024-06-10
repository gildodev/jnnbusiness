from django.contrib.sitemaps import Sitemap
from .models import Produto

class ProdutoSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Produto.objects.all()

    def lastmod(self, obj):
        return obj.data_create
    

    def location(self, obj):
        return obj.get_absolute_url()
