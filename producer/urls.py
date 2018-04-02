from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^edit_brand/$', views.edit_brand),
	url(r'^edit_product/$', views.edit_product),
	url(r'^edit_item/$', views.edit_item),
	url(r'^login/$',views.producer_login),
	url(r'^delete_brand/$',views.delete_brand),
	url(r'^delete_product/$',views.delete_product),
	url(r'^delete_item/$',views.delete_item),
	url(r'^ongoing_orders/$', views.get_ongoing_orders),
	url(r'^completed_orders/$', views.get_completed_orders),
	url(r'^change_status/$', views.status_change),
	url(r'^product_description/$', views.product_description),
	url(r'^item_description/$', views.item_description),
]