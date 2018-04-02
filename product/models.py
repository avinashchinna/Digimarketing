# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Brand(models.Model):

	brand_id = models.AutoField("Brand ID", db_column = 'brand_id', primary_key = True)
	brand_name = models.CharField("Brand Name", max_length = 50)

	class Meta:
		db_table = 'brand'

	def __unicode__(self):
		return unicode(self.brand_name)


class Product(models.Model):

	product_id = models.AutoField("Product ID", db_column = 'product_id', primary_key = True)
	product_name = models.CharField("Product Name", max_length = 50)
	brand = models.ForeignKey(Brand, db_column = 'brand', on_delete = models.CASCADE)
	offers = models.TextField("Offers", blank = True)
	description = models.TextField("Description", blank = True)
	additional_info = models.TextField("Additional Info", blank = True) 

	class Meta:
		db_table = 'product'

	def __unicode__(self):
		return unicode(self.product_name)


class Item(models.Model):

	item_id = models.AutoField("Item ID ", db_column = 'item_id', primary_key = True)
	item_name = models.CharField("Item Name", max_length = 50)
	product = models.ForeignKey(Product, db_column = 'product', on_delete = models.CASCADE)
	item_cost = models.PositiveSmallIntegerField("Item Cost")

	class Meta:
		db_table = 'item'

	def __unicode__(self):
		return unicode(self.item_name)