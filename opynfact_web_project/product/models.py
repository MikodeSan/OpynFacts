from django.db import models
from django.contrib.auth import get_user_model


# class ZContact(models.Model):
#     name = models.CharField(max_length=200)
#     email = models.EmailField(max_length=100)

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = "Utilisateur"
#         verbose_name_plural = "Utilisateurs"


class ZProduct(models.Model):
    reference = models.BigIntegerField('Code', null=True, unique=True)
    brands = models.CharField('Marque', max_length=200)
    name = models.CharField('Nom', max_length=200)
    store = models.IntegerField(null=True)
    category_hierarchy = models.IntegerField(null=True)
    nutrition_grade = models.IntegerField(null=True)
    nova_group = models.IntegerField(null=True)
    url = models.URLField()
    picture = models.URLField()
    last_modified = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    isSearched = models.BooleanField(default=False)
    firstSearchDate = models.DateTimeField(auto_now_add=True)
    lastSearchDate = models.DateTimeField(auto_now_add=True)
    
    isfavorite = models.BooleanField(default=False)

    searchers = models.ManyToManyField(get_user_model(), through='ZSearch', related_name='searches', blank=True)
    users = models.ManyToManyField(get_user_model(), through='ZFavorite', related_name='favorites', blank=True)
    alternatives = models.ManyToManyField('self', related_name='substituted', symmetrical=False, blank=True)

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        constraints = [
            models.UniqueConstraint(fields=['reference', 'brands', 'name'], name='product_identifier_unique'),
        ]

    def __str__(self):
        return "{} - {} - {}".format(self.reference, self.brands, self.name)


class ZFavorite(models.Model):
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    favorite = models.ForeignKey(ZProduct, on_delete=models.CASCADE)
    # alternatives = models.ManyToManyField(ZFavorite, related_name='zsearches', blank=True)


class ZSearch(models.Model):
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    target = models.ForeignKey(ZProduct, on_delete=models.CASCADE)
    favorite_alternatives = models.ManyToManyField(ZFavorite, related_name='zsearches', blank=True)


class ZCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)
    product = models.ManyToManyField(ZProduct, related_name='category', blank=True)

    def __str__(self):
        return self.name


# class Booking(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     contacted = models.BooleanField(default=False)
#     album = models.OneToOneField(Album)
#     contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
