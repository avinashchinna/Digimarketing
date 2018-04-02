# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from product.models import Brand, Product, Item

from dbHandler import pgExecQuery, pgExecUpdate
# Create your views here.

@csrf_exempt
def add_brand(request):

	if request.method == 'POST':
		try:

			reqdata = json.loads(request.body.decode("utf-8"))
			if not reqdata["brand_name"]:
				return JsonResponse({"status": False, "msg": "Brand name shouldn't be empty"})
			if Brand.objects.filter(brand_name = reqdata["brand_name"]).exists():
				return JsonResponse({"status": False, "msg": "Given Brand already exists"})

			query = "insert into brand (brand_name) values (%s)"
			pgExecUpdate(query,[reqdata["brand_name"]])
			
			return JsonResponse({"status" : True})
		except :
			return JsonResponse({"status" : False})


@csrf_exempt
def add_product(request):

	if request.method == 'POST':
		try:

			reqdata = json.loads(request.body.decode("utf-8"))
			if not reqdata["product_name"]:
				return JsonResponse({"status": False, "msg": "Product name shouldn't be empty"})
			if Product.objects.filter(product_name = reqdata["product_name"]).exists():
				return JsonResponse({"status": False, "msg": "Given Product already exists"})
			if not reqdata["brand"]:
				return JsonResponse({"status": False, "msg": "Brand name shouldn't be empty"})
			if not Brand.objects.filter(brand_name = reqdata["brand"]).exists():
				return JsonResponse({"status": False, "msg": "Brand doesn't exist"})

			brand = Brand.objects.get(brand_name = reqdata["brand"])

			query = "insert into product (product_name, brand, offers, description, additional_info) values (%s, %s, %s, %s, %s)"
			pgExecUpdate(query,[reqdata["product_name"], brand.brand_id, reqdata["offers"], reqdata["description"], reqdata["additional_info"]])
			
			return JsonResponse({"status" : True})
		except :
			return JsonResponse({"status" : False})


@csrf_exempt
def add_item(request):

	if request.method == 'POST':
		try:

			reqdata = json.loads(request.body.decode("utf-8"))
			if not reqdata["item_name"]:
				return JsonResponse({"status": False, "msg": "Item name shouldn't be empty"})
			if not reqdata["product"]:
				return JsonResponse({"status": False, "msg": "Product name shouldn't be empty"})
			if not reqdata["item_cost"]:
				return JsonResponse({"status": False, "msg": "Item Cost shouldn't be empty"})
			if Item.objects.filter(item_name = reqdata["item_name"]).exists():
				return JsonResponse({"status": False, "msg": "Given Item already exists"})
			if not Product.objects.filter(product_name = reqdata["product"]).exists():
				return JsonResponse({"status": False, "msg": "Product doesn't exist"})

			product = Product.objects.get(product_name = reqdata["product"])

			query = "insert into item (item_name, product, item_cost) values (%s, %s, %s)"
			pgExecUpdate(query,[reqdata["item_name"], product.product_id, reqdata["item_cost"]])
			
			return JsonResponse({"status" : True})
		except :
			return JsonResponse({"status" : False})