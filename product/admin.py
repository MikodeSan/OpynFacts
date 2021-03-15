from django.contrib import admin

from .models import ZProduct

# Register your models here.
# admin.site.register(ZProduct)
@admin.register(ZProduct)
class ZProductAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "code",
                    "brands",
                    "name",
                    "stores",
                    "nutrition_grades",
                    "nova_group",
                    "nutrition_score",
                    "nutrition_score_beverage",
                    "unique_scans_n",
                    "created_t",
                    "last_modified_t",
                    "update_t",
                    "image_url",
                    "alternatives",
                ]
            },
        )
    ]  # list columns
    readonly_fields = ["created_t", "update_t"]

    def has_add_permission(self, request):
        return False


class ZProductInline(admin.TabularInline):
    model = ZProduct
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "code",
                    "brands",
                    "name",
                    "stores",
                    "nutrition_grades",
                    "nova_group",
                    "nutrition_score",
                    "nutrition_score_beverage",
                    "unique_scans_n",
                    "created_t",
                    "last_modified_t",  # 'update_t',
                    "image_url",
                    "alternatives",
                ]
            },
        )
    ]  # list columns


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
