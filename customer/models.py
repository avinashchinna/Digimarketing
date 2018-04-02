# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from product.models import Item

# Create your models here.

class Customer(models.Model):

	user = models.OneToOneField(User, primary_key = True, db_column = 'user_id', on_delete = models.CASCADE)
	# User: *username, *password, *first_name, last_name, *email
	mobile = models.CharField("Mobile Number", max_length = 11, default = '9876543210')
	address = models.TextField("Address")
	time_stamp = models.DateTimeField(auto_now = True, blank = True, null = True)

	class Meta:
		db_table = 'customer'

	def __unicode__(self):
		return unicode(self.user)

class Order(models.Model):

	STATUS_PENDING = '0'
	STATUS_RECEIVED = '1'
	STATUS_DISPATCHED = '2'
	STATUS_DELIVERED = '3'
	STATUS_CANCELLED = '4'
	STATUS_CANCELLED_BY_VENDOR = '5'

	STATUS_CHOICES = (
		(STATUS_PENDING, 'Pending'),
		(STATUS_RECEIVED, 'Received'),
		(STATUS_DISPATCHED, 'Dispatched'),
		(STATUS_DELIVERED, 'Delivered'),
		(STATUS_CANCELLED, 'Cancelled'),
		(STATUS_CANCELLED_BY_VENDOR, 'Cancelled by Vendor'),
	)

	order_id = models.AutoField("Order ID", db_column = 'order_id', primary_key = True)
	customer = models.ForeignKey(Customer, db_column = 'customer', on_delete = models.CASCADE)
	item = models.ForeignKey(Item, db_column = 'item', on_delete = models.CASCADE)
	quantity = models.PositiveSmallIntegerField("Quantity", blank = True)
	order_cost = models.IntegerField("Order Cost", blank = True)
	status = models.CharField("Status of Order", choices = STATUS_CHOICES, max_length = 1, blank = True, default = STATUS_PENDING)
	time_stamp = models.DateTimeField(auto_now_add = True)

	class Meta:
		db_table = 'orders'

	def __unicode__(self):
		return unicode(self.item)

