from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^register/$', views.register),
	url(r'^login/$', views.user_login),
	url(r'^logout/$', views.user_logout),
	url(r'^fetchbrands/$', views.get_all_brands),
	url(r'^fetchproducts/$', views.get_all_products_of_brand),
	url(r'^fetchitems/$', views.get_all_items_of_product),
	url(r'^product_description/$', views.product_description),
	url(r'^placeorder/$', views.place_order),
	url(r'^allorders/$', views.get_all_orders),
	url(r'^cancelorder/$', views.cancel_order),
	url(r'^getorderstatus/$', views.get_order_status),
]