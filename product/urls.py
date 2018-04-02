from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^add_brand/$', views.add_brand),
	url(r'^add_product/$', views.add_product),
	url(r'^add_item/$', views.add_item),
]