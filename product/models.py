from django.db import models
from django.contrib.auth import get_user_model


class ZProduct(models.Model):
    code = models.BigIntegerField('Code', primary_key=True, default=0, null=False, unique=True)
    brands = models.CharField('Marque', max_length=256, null=True)
    name = models.CharField('Nom', max_length=256)
    url = models.URLField('URL', null=True)
    stores = models.CharField('Stores', max_length=256, null=True)
    # category_hierarchy = models.IntegerField(null=True)
    nutrition_grades = models.CharField('Nutri-Score', max_length=1, null=True)
    nova_group = models.SmallIntegerField('Nova', null=True)
    nutrition_score_fr = models.SmallIntegerField('Nutrition score', null=True)
    nutrition_score_uk = models.SmallIntegerField('Nutrition score', null=True)
    nutrition_score_beverage = models.SmallIntegerField('Nutrition score beverage', null=True)
    fat_100g = models.FloatField('Matières grasses / Lipides', null=True)
    saturated_fat_100g = models.FloatField('Acides gras saturés', null=True)
    sugars_100g = models.FloatField('Sucres', null=True)
    salt_100g = models.FloatField('Sel', null=True)
    unique_scans_n = models.SmallIntegerField('Popularité', null=True)
    created_t = models.BigIntegerField('Date de création', null=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    last_modified_t = models.BigIntegerField('Date de mise à jour', null=False, default=0)
    # last_modified = models.DateTimeField(auto_now_add=True)
    update_t = models.DateTimeField("Date d'enregistrement", auto_now_add=True, null=True)
    image_url = models.URLField('Image URL', null=True)
    
    categories = models.ManyToManyField('ZCategory', through='ZCategory_Product', related_name='products', blank=True)
    searchers = models.ManyToManyField(get_user_model(), through='ZSearch', related_name='searches', blank=True)
    users = models.ManyToManyField(get_user_model(), through='ZFavorite', related_name='favorites', blank=True)
    alternatives = models.ManyToManyField('self', related_name='substituted', symmetrical=False, blank=True)

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        # constraints = [
        #     models.UniqueConstraint(fields=['brands', 'name'], name='product_identifier_unique'),
        # ]

    def __str__(self):
        return "{} - {} - {}".format(self.code, self.brands, self.name)


class ZCategory(models.Model):
    identifier = models.CharField(max_length=256, primary_key=True, unique=True)
    label = models.CharField(max_length=256, null=True)

    def __str__(self):
        return "{} - {}".format(self.identifier, self.label)

class ZCategory_Product(models.Model):
    product = models.ForeignKey('ZProduct', on_delete=models.CASCADE)
    category = models.ForeignKey('ZCategory', on_delete=models.CASCADE)

    hierarchy_index = models.PositiveSmallIntegerField(default=0, null=False)
    date = models.DateTimeField(auto_now=True)

    # alternatives = models.ManyToManyField(ZFavorite, related_name='zsearches', blank=True)

class ZFavorite(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    favorite = models.ForeignKey('ZProduct', on_delete=models.CASCADE)
    # alternatives = models.ManyToManyField(ZFavorite, related_name='zsearches', blank=True)

    date = models.DateTimeField(auto_now=True)

class ZSearch(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    target = models.ForeignKey('ZProduct', on_delete=models.CASCADE)
    favorite_alternatives = models.ManyToManyField(ZFavorite, related_name='zsearches', blank=True)

    date = models.DateTimeField(auto_now=True)


# class Booking(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     contacted = models.BooleanField(default=False)
#     album = models.OneToOneField(Album)
#     contact = models.ForeignKey(Contact, on_delete=models.CASCADE)


# class ZContact(models.Model):
#     name = models.CharField(max_length=200)
#     email = models.EmailField(max_length=100)

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = "Utilisateur"
#         verbose_name_plural = "Utilisateurs"
