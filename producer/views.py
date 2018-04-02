# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from customer.models import *
from product.models import *

from dbHandler import pgExecQuery, pgExecUpdate

# Create your views here.
@csrf_exempt
def producer_login(request):

	if request.method == 'POST':
		try:
			reqdata = json.loads(request.body.decode("utf-8"))
			user = authenticate(username = reqdata['username'],
			 password = reqdata['password'])
			if user is not None:
				if user.is_superuser:
					login(request, user)
					return JsonResponse({"status": True , "msg": "admin login"})
			return JsonResponse({"status": False, "msg": "Invalid Credentials"})
		except:
			return JsonResponse({"status": False})

	if request.method == 'GET':
		pass


@csrf_exempt
def edit_brand(request):

	if request.method == 'POST':
		try:

			reqdata = json.loads(request.body.decode("utf-8"))
			if not reqdata["brand_name"]:
				return JsonResponse({"status": False, "msg": "Brand name shouldn't be empty"})

			query = "update brand set brand_name = %s where brand_id = %s "
			pgExecUpdate(query,[reqdata["brand_name"],reqdata["brand_id"]])
			
			return JsonResponse({"status" : True})
		except :
			return JsonResponse({"status" : False})


@csrf_exempt
def edit_product(request):

	if request.method == 'POST':
		try:

			reqdata = json.loads(request.body.decode("utf-8"))
			if not reqdata["product_name"]:
				return JsonResponse({"status": False, "msg": "Product name shouldn't be empty"})
			if not reqdata["brand"]:
				return JsonResponse({"status": False, "msg": "Brand name shouldn't be empty"})

			brand = Brand.objects.get(brand_name = reqdata["brand"])

			query = "update product set product_name = %s, brand = %s, offers = %s, description = %s, additional_info = %s where product_id = %s"
			pgExecUpdate(query,[reqdata["product_name"], brand.brand_id, reqdata["offers"], reqdata["description"], reqdata["additional_info"], reqdata["product_id"]])
			
			return JsonResponse({"status" : True})
		except :
			return JsonResponse({"status" : False})


@csrf_exempt
def edit_item(request):

	if request.method == 'POST':
		
		try:

			reqdata = json.loads(request.body.decode("utf-8"))
			if not reqdata["item_name"]:
				return JsonResponse({"status": False, "msg": "Item name shouldn't be empty"})
			if not reqdata["product"]:
				return JsonResponse({"status": False, "msg": "Product name shouldn't be empty"})
			if not reqdata["item_cost"]:
				return JsonResponse({"status": False, "msg": "Item Cost shouldn't be empty"})
			if not Product.objects.filter(product_name = reqdata["product"]).exists():
				return JsonResponse({"status": False, "msg": "Product doesn't exist"})

			product = Product.objects.get(product_name = reqdata["product"])

			query = "update item set item_name = %s, product = %s, item_cost = %s where item_id = %s"
			pgExecUpdate(query,[reqdata["item_name"], product.product_id, reqdata["item_cost"], reqdata["item_id"]])
			
			return JsonResponse({"status" : True})
		except :
			return JsonResponse({"status" : False})


@csrf_exempt
def delete_brand(request):

	if request.method == 'POST':

		try:

			reqdata = json.loads(request.body.decode("utf-8"))
			if not Brand.objects.filter(brand_id = reqdata["brand_id"]).exists():
				return JsonResponse({"status": False, "msg": "Brand doesn't exist"})

			query = "delete from brand where brand_id = %s"
			pgExecUpdate(query,[reqdata["brand_id"]])
			return JsonResponse({"status" : True, "msg" : "brand deleted"})

		except:
			return JsonResponse({"status" : False, "msg" : "internal error"})


@csrf_exempt
def delete_product(request):

	if request.method == 'POST':

		try:

			reqdata = json.loads(request.body.decode("utf-8"))
			if not Product.objects.filter(product_id = reqdata["product_id"]).exists():
				return JsonResponse({"status": False, "msg": "Product doesn't exist"})

			query = "delete from product where product_id = %s"
			pgExecUpdate(query,[reqdata["product_id"]])
			return JsonResponse({"status" : True, "msg" : "product deleted"})

		except:
			return JsonResponse({"status" : False, "msg" : "internal error"})


@csrf_exempt
def delete_item(request):

	if request.method == 'POST':

		try:

			reqdata = json.loads(request.body.decode("utf-8"))
			if not Item.objects.filter(item_id = reqdata["item_id"]).exists():
				return JsonResponse({"status": False, "msg": "Item doesn't exist"})

			query = "delete from item where item_id = %s"
			try:
				pgExecUpdate(query,[reqdata["item_id"]])
			except:
				return JsonResponse({"status" : True , "msg" : "internal error"})
			
			return JsonResponse({"status" : True, "msg" : "item deleted"})

		except:
			return JsonResponse({"status" : False, "msg" : "internal error"})


@csrf_exempt
def get_ongoing_orders(request):

	try:
		
		resp = {"status": True}
		resp["ongoing_orders"] = []
		orders = Order.objects.all().filter(status__in = ['0', '1', '2']).order_by('customer')
		for order in orders:
			odict = {
				"order_id": order.order_id,
				"cust_id" : order.customer.user.id,
				"customer" : order.customer.user.first_name,
				"mobile" : order.customer.mobile,
				"address": order.customer.address,
				"brand" : order.item.product.brand.brand_name,
				"product" : order.item.product.product_name,
				"item_name": order.item.item_name,
				"order_cost": order.order_cost,
				"quantity": order.quantity,
				"order_status" : order.get_status_display(),
			}
			resp["ongoing_orders"].append(odict)
		return JsonResponse(resp)

	except:
		return JsonResponse({"status": False})


@csrf_exempt
def get_completed_orders(request):

	try:
		resp = {"status": True}
		resp["completed_orders"] = []
		orders = Order.objects.all().filter(status__in = ['3', '4', '5']).order_by('-time_stamp')
		for order in orders:
			odict = {
				"order_id": order.order_id,
				"customer" : order.customer.user.first_name,
				"mobile" : order.customer.mobile,
				"address": order.customer.address,
				"brand" : order.item.product.brand.brand_name,
				"product" : order.item.product.product_name,
				"item_name": order.item.item_name,
				"order_cost": order.order_cost,
				"quantity": order.quantity,
				"order_status" : order.get_status_display(),
			}
			resp["completed_orders"].append(odict)
		return JsonResponse(resp)

	except:
		return JsonResponse({"status": False})


@csrf_exempt
def status_change(request):
	try:
		reqdata = json.loads(request.body.decode("utf-8"))
		order_ids = reqdata["order_ids"]
		for order_id in order_ids:
			qry = "select status from orders where order_id = %s"
			resultset = pgExecQuery(qry, [order_id])
			if resultset[0].status != Order.STATUS_CANCELLED:
				qry = "update orders set status = %s where order_id = %s"
				pgExecUpdate(qry, [reqdata["status"], order_id])

		return JsonResponse({"status" : True, "msg" : "Success", "order_id" : order_id, "statuschange" : reqdata["status"]})

	except:
		return JsonResponse({"status" : False, "msg" : "Failed"})


@csrf_exempt
def product_description(request):

	if request.method == 'POST':

		try:
			reqdata = json.loads(request.body.decode("utf-8"))
			resp = {"status": True}
			product = Product.objects.get(product_id = reqdata["product_id"])
			resp["product_name"] = product.product_name
			resp["brand_name"] = product.brand.brand_name
			resp["offers"] = product.offers
			resp["description"] = product.description
			resp["additional_info"] = product.additional_info
			return JsonResponse(resp)
		except:
			return JsonResponse({"status": False})
	else:
		return JsonResponse({"status": False})


@csrf_exempt
def item_description(request):

	if request.method == 'POST':

		try:
			reqdata = json.loads(request.body.decode("utf-8"))
			resp = {"status": True}
			item = Item.objects.get(item_id = reqdata["item_id"])
			resp["item_name"] = item.item_name
			resp["item_cost"] = item.item_cost
			return JsonResponse(resp)
		except:
			return JsonResponse({"status": False})
	else:
		return JsonResponse({"status": False})