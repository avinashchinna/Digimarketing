# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from product.models import Brand, Product, Item

class BrandAdmin(admin.ModelAdmin):
	list_display = ('brand_id', 'brand_name')

class ProductAdmin(admin.ModelAdmin):
	list_display = ('product_id', 'product_name', 'brand', 'offers', 'description', 'additional_info')
	fields = ('product_name', 'brand', 'offers', 'description', 'additional_info')

class ItemAdmin(admin.ModelAdmin):
	list_display = ('item_id', 'item_name', 'product', 'item_cost')
	fields = ('item_name', 'product', 'item_cost')

admin.site.register(Brand)
admin.site.register(Product, ProductAdmin)
admin.site.register(Item, ItemAdmin)
