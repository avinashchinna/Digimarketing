# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from customer.models import Customer, Order

class CustomerAdmin(admin.ModelAdmin):
	list_display = ('user', 'mobile', 'address', 'time_stamp')
	fields = ('user', 'mobile', 'address')

class OrderAdmin(admin.ModelAdmin):
	list_display = ('order_id', 'customer', 'item', 'quantity', 'order_cost', 'status', 'time_stamp')
	fields = ('customer', 'item', 'quantity', 'order_cost', 'status')

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
