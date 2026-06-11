from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class CodeConverterSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5
    def items(self):
        # List all the named URLs you want to include
        return ['code_converter:index', 'code_converter:convert_code', 'code_converter:auto_test']
    def location(self, item):
        return reverse(item)