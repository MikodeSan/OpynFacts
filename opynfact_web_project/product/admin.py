from django.contrib import admin

from .models import ZProduct 

# Register your models here.
# admin.site.register(ZProduct)
@admin.register(ZProduct)
class ZProductAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['reference', 'brand', 'name']})
        ] # list columns
    readonly_fields = ["created_at"]

    def has_add_permission(self, request):
        return False

class ZProductInline(admin.TabularInline):
    model = ZProduct
    fieldsets = [
        (None, {'fields': ['reference', 'brand', 'name']})
        ] # list columns

# class ZContactProductInline(admin.TabularInline):
#     model = ZContact.favorite.through # the query goes through an intermediate table.

#     verbose_name = "Favori"
#     verbose_name_plural = "Favoris"
    
#     extra = 1

# @admin.register(ZContact)
# class ZContactAdmin(admin.ModelAdmin):
#     search_fields = ['name', 'email']
#     list_filter = ['name', 'email']
#     inlines = [ZContactProductInline,] # list of bookings made by a contact
