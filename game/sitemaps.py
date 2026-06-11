from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class GameSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5
    def items(self):
        # List all the named URLs you want to include
        return ['game:index']
    def location(self, item):
        return reverse(item)