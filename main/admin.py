from django.contrib import admin
from django.apps import apps
from .models import *

@admin.register(Image)
class ImageModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'img_preview']
    readonly_fields = ["img_preview"]  

# @admin.register(Product)
# class ProductModelAdmin(admin.ModelAdmin):
#     list_display = ["name" , "price" , "discounted_price" , "mean_rate_star_data", "get_categories" , "subcategory", "vendor_code", "in_stock"]
#     list_display_links = ["name" , "price" , "discounted_price" ,  "mean_rate_star_data", "get_categories" , "subcategory", "vendor_code", "in_stock"]
#     search_fields = Product._meta.get_fields()
#     date_hierarchy = 'creation_time'
#     list_per_page = 10
#     list_filter =  ["name" , "price" , "discounted_price" , "mean_rate_star_data", "get_categories" , "subcategory", "vendor_code", "in_stock"]

    

#     def get_categories(self, obj):
#         return ", ".join([category.name for category in obj.categories.all()])

#     get_categories.short_description = "Categories"

#     def get_form(self, request, obj=None, **kwargs):
#         form = super().get_form(request, obj, **kwargs)

#         class CustomProductForm(form):
#             class Meta(form.Meta):
#                 model = Product

#             def clean(self):
#                 cleaned_data = super().clean()
#                 price = cleaned_data.get('price')
#                 discount = cleaned_data.get('discount')

#                 if price is not None and discount is not None:
#                     cleaned_data['discounted_price'] = round(price - (price * (discount / 100)), 2)

#                 return cleaned_data

#         return CustomProductForm



@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "get_discounted_price", "mean_rate_star_data",  "vendor_code", "in_stock"] # - category . subcategory
    list_display_links = ["name", "price", "get_discounted_price", "mean_rate_star_data",  "vendor_code", "in_stock"]# - category
    search_fields = ["name", "categories__name", "subcategory", "vendor_code"]
    date_hierarchy = 'created_at'
    list_per_page = 10
    list_filter =  ["name" , "price" ,  "mean_rate_star_data",  "subcategory", "vendor_code", "in_stock"]


    def get_discounted_price(self, obj):
        return obj.discounted_price

    get_discounted_price.short_description = "Discounted Price"

    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])

    display_categories.short_description = "Categories"


    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        class CustomProductForm(form):
            class Meta(form.Meta):
                model = Product

            def clean(self):
                cleaned_data = super().clean()
                price = cleaned_data.get('price')
                discount = cleaned_data.get('discounted_price')

                if price is not None and discount is not None:
                    cleaned_data['discounted_price'] = round(price - (price * (discount / 100)), 2)

                return cleaned_data

        return CustomProductForm

@admin.register(Review)
class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ['user' , 'product', 'star' , "created_at"]
    list_display_links = ['user' , 'product', 'star', "created_at"]
    search_fields = Review._meta.get_fields()
    list_filter = ['user' , 'product']
    date_hierarchy = 'created_at'




#-------------------------------------------Auto-Register----------------------------------------------------
models = apps.get_models()

for model in models:
    try:
        admin.site.register(model_or_iterable=model)
    except admin.sites.AlreadyRegistered:
        pass

#------------------------------------------------------------------------------------------------------------




