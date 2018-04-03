# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import traceback

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
from customer.models import *
from product.models import *

from dbHandler import *
# Create your views here.

@csrf_exempt
def createsu(request):
	if request.method == 'POST':
		try:
			reqdata = json.loads(request.body.decode("utf-8"))
			User.objects.create_superuser(reqdata['username'], '', reqdata['password'])
			return JsonResponse({"status": True})
		except:
			return JsonResponse({"status": False})

@csrf_exempt
def register(request):

	if request.method == 'POST':
		try:
			reqdata = json.loads(request.body.decode("utf-8"))
			if not reqdata['username']:
				return JsonResponse({"status": False, "msg": "Username shouldn't be empty"})
			if User.objects.filter(username = reqdata['username']).exists():
				return JsonResponse({"status": False, "msg": "Given Username already in use"})
			if User.objects.filter(email = reqdata['email']).exists():
				return JsonResponse({"status": False, "msg": "Given email already in use"})
			if not reqdata['password']:
				return JsonResponse({"status": False, "msg": "Password cannot be empty"})
			if not reqdata['address']:
				return JsonResponse({"status": False, "msg": "Address cannot be empty"})

			user = User()
			user.username = reqdata['username']
			user.first_name = reqdata['cust_name']
			user.email = reqdata['email']
			user.set_password(reqdata['password'])
			try:
				user.save()
			except:
				return JsonResponse({"status": False, "msg": "Internal Server Error"})
			
			customer = Customer()
			customer.user = user
			customer.mobile = reqdata['mobile']
			customer.address = reqdata['address']
			try:
				customer.save()
			except:
				user.delete()
				return JsonResponse({"status": False, "msg": "Internal Server Error"})

			return JsonResponse({"status": True, "msg": "Registered Successfully"})
		except:
			return JsonResponse({"status": False})

	if request.method == 'GET':
		pass


@csrf_exempt
def user_login(request):

	if request.method == 'POST':
		try:
			reqdata = json.loads(request.body.decode("utf-8"))
			user = authenticate(username = reqdata['username'],
			 password = reqdata['password'])
			if user:
				login(request, user)
				return JsonResponse({"status": True, "msg": "logged in Successfully"})
			return JsonResponse({"status": False, "msg": "Invalid Credentials"})
		except:
			return JsonResponse({"status": False})

	if request.method == 'GET':
		pass


@csrf_exempt
def user_logout(request):
	logout(request)
	return JsonResponse({"status": True , "msg": "logged out successfully"})


@csrf_exempt
def get_all_brands(request):

	try:
		resp = {"status": True}
		resp["brands"] = []
		query = "select brand_id, brand_name from brand order by brand_name"
		resultset = pgExecQuery(query)
		for res in resultset:
			resp["brands"].append({"id": res.brand_id, "name": res.brand_name})
		return JsonResponse(resp)
	except:
		return JsonResponse({"status": False})


@csrf_exempt
def get_all_products_of_brand(request):

	if request.method == 'POST':
		try:
			reqdata = json.loads(request.body.decode("utf-8"))
			resp = {"status": True}
			resp["products"] = []
			brand = Brand.objects.get(brand_name = reqdata["brand"])
			query = "select product_id, product_name from product where brand = %s"
			resultset = pgExecQuery(query, [brand.brand_id])
			for res in resultset:
				resp["products"].append({"id": res.product_id, "name": res.product_name})
			return JsonResponse(resp)
		except:
			return JsonResponse({"status": False})
	else:
		return JsonResponse({"status": False})


@csrf_exempt
def get_all_items_of_product(request):

	if request.method == 'POST':
		try:
			reqdata = json.loads(request.body.decode("utf-8"))
			resp = {"status": True}
			resp["items"] = []
			product = Product.objects.get(product_name = reqdata["product"])
			query = "select * from item where product = %s"
			resultset = pgExecQuery(query, [product.product_id])
			for res in resultset:
				resp["items"].append({"id": res.item_id, "name": res.item_name, "cost": res.item_cost})
			return JsonResponse(resp)
		except:
			return JsonResponse({"status": False})
	else:
		return JsonResponse({"status": False})


@csrf_exempt
def product_description(request):

	if request.method == 'POST':

		try:
			reqdata = json.loads(request.body.decode("utf-8"))
			resp = {"status": True}
			resp["items"] = []
			product = Product.objects.get(product_name = reqdata["product"])
			query = "select item_id, item_name from item where product = %s"
			resultset = pgExecQuery(query, [product.product_id])
			for res in resultset:
				resp["items"].append({"id": res.item_id, "name": res.item_name})
			resp["product_name"] = reqdata["product"]
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
def place_order(request):

	if request.method == 'POST':
		try:
			reqdata = json.loads(request.body.decode("utf-8"))			
			resp = {"status": True}
			resp["order_ids"] = []
			for item in reqdata["items"]:
				qry = "select item_cost from item where item_id = %s"
				resultset = pgExecQuery(qry, [item["id"]])
				cost = resultset[0].item_cost * item["quantity"]
				print(request.user.id, item["id"], item["quantity"], cost, Order.STATUS_PENDING)
				qry = "insert into orders(customer, item, quantity, order_cost, status, time_stamp) values (%s,%s,%s,%s,%s,now()) returning order_id"
				resultset = pgExecQuery(qry, [request.user.id, item["id"], item["quantity"], cost, Order.STATUS_PENDING])
				resp["order_ids"].append(resultset[0].order_id)
			return JsonResponse(resp)			
		except:
			return JsonResponse({"status": False, "msg": "Unknown Error Occured"})

	else:
		return JsonResponse({"status": False})


@csrf_exempt
def get_ongoing_orders(request):

	try:
		resp = {"status": True}
		resp["ongoing_orders"] = []
		resp["completed_orders"] = []
		orders = Order.objects.all().filter(customer = request.user.id, status__in = ['0', '1', '2']).order_by('-time_stamp')
		for order in orders:
			odict = {
				"order_id": order.order_id,
				"brand" : order.item.product.brand.brand_name,
				"product" : order.item.product.product_name,
				"item_name": order.item.item_name,
				"order_cost": order.order_cost,
				"quantity": order.quantity,
				"order_status" : order.get_status_display(),
				"showcb": False,
			}
			if((timezone.now() - order.time_stamp).total_seconds() < 3600):
				odict["showcb"] = True
			
			resp["ongoing_orders"].append(odict)
		return JsonResponse(resp)
	except:
		return JsonResponse({"status": False})


@csrf_exempt
def get_completed_orders(request):

	try:
		resp = {"status": True}
		resp["ongoing_orders"] = []
		resp["completed_orders"] = []
		orders = Order.objects.all().filter(customer = request.user.id, status__in = ['3', '4', '5']).order_by('-time_stamp')
		for order in orders:
			odict = {
				"order_id": order.order_id,
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
def get_order_status(request):

	if request.method == 'POST':
		try:
			reqdata = json.loads(request.body.decode("utf-8"))
			resp = {"status": True}
			resp["statlist"] = []
			for orderid in reqdata["order_ids"]:
				order = Order.objects.get(order_id = orderid)
				resp["statlist"].append(order.get_status_display())
			return JsonResponse(resp)
		except:
			return JsonResponse({"status": False})

	else:
		return JsonResponse({"status": False, "msg": "Expected method = HTTP POST"})


@csrf_exempt
def cancel_order(request):

	if request.method == 'POST':
		try:
			reqdata = json.loads(request.body.decode("utf-8"))
			order = Order.objects.get(order_id = reqdata["order_id"])
			if((timezone.now() - order.time_stamp).total_seconds() > 3600):
				return JsonResponse({"status": False, "msg" : "It's already been 1 hour after order got placed"})
			qry = "update orders set status = %s where order_id = %s"
			pgExecUpdate(qry, [Order.STATUS_CANCELLED, reqdata["order_id"]])
			return JsonResponse({"status": True})
		except:
			return JsonResponse({"status": False})

	else:
		return JsonResponse({"status": False})


@csrf_exempt
def get_profile(request):

	try:
		resp = {"status": True}
		customer = Customer.objects.get(user_id = request.user.id)
		resp["email"] = customer.user.email
		resp["name"] = customer.user.first_name
		resp["username"] = customer.user.username
		resp["mobile"] = customer.mobile
		resp["address"] = customer.address
		return JsonResponse(resp)
	except:
		return JsonResponse({"status": False})
