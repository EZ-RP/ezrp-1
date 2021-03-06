from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main, name='stock_Main'),
    url(r'^stock/all_available/$', views.all_stock, name='all_available'),
    url(r'^stock_form/$', views.stockform, name='stock_form'),
    url(r'^stock/delete/(?P<lineid>\d+)/$', views.stock_delete, name='stock_delete'),
    url(r'^stock/edit/(?P<lineid>\d+)/$', views.stock_edit, name='stock_edit'),
    url(r'^stock/all_stock/$', views.all_stock, name='all_stock'),

]