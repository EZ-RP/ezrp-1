from django.shortcuts import render
from django.views.generic import ListView
from order.models import Order
from order.models import OrderLine
from order.models import Discounts
from .modelforms import OrderForm
from .modelforms import LineForm
from .modelforms import DiscountForm
from django.http import HttpResponse
from django_tables2 import RequestConfig
from order.tables import SaleTable
# Create your views here.


def sales(request):
    return render(request, 'order/Sales/sales.html')


def purchases(request):
    return render(request, 'order/Purchases/purchases.html')


def setup(request):
    return render(request, 'order/orderSetup.html')


def all_discounts(request):
    discs = Discounts(Discounts.objects.all())
    RequestConfig(request).configure(discs)
    return render(request, 'order/Sales/all_discounts.html', {'discounts': discs})


def all_sales(request):
    saless = SaleTable(Order.objects.filter(order_type="S"))
    RequestConfig(request).configure(saless)
    return render(request, 'order/Sales/all_salesOrders.html', {'sales': saless})
    # return render(request, 'order/Sales/all_salesOrders.html',
    #             {'sales': Order.objects.filter(order_type="S")})


def all_saleslines(request):
    return render(request, 'order/Sales/all_salesLines.html',
                  {'saleslines': OrderLine.objects.all()})


def single_sales(request):
    return render(request, 'order/Sales/all_salesOrders.html',
                  {'sales': Order.objects.filter(order_number=1)})


def all_purchases(request):
    return render(request, 'order/Purchases/all_purchaseOrders.html',
                  {'purchases': Order.objects.filter(order_type="P")})


def sale(request, order_number):
    singlesale = Order.objects.get(order_number=order_number, order_type='S')
    form_order = OrderForm(instance=singlesale)
    return render(request, 'order/Sales/sale.html', {'form_sale': form_order})


def new_discount(request):
    if request.method == "POST":
        form = DiscountForm(request.POST)
        if form.is_valid():
            form.save()
            #order = form.save(commit=False)
            #order.order_type = 'S'
            #order.save()
            form = DiscountForm()
    else:
        form = DiscountForm()
    return render(request, 'order/Sales/new_discount.html', {'form': form})


def sale_new(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.order_type = 'S'
            order.save()
            form = OrderForm()
    else:
        form = OrderForm()
    return render(request, 'order/Sales/sale_new.html', {'form': form})


def saleline_new(request):
    if request.method == "POST":
        form = LineForm(request.POST)
        if form.is_valid():
            orderline = form.save(commit=False)
            orderline.order_number = Order.objects.get(order_number=1)
            if OrderLine.objects.count() > 0:
                orderline.order_line_id = OrderLine.objects.latest('order_line_id')
            else:
                orderline.order_line_id = 1
            orderline.save()
            form = LineForm()
    else:
        form = LineForm()
    return render(request, 'order/Sales/saleline_new.html', {'form': form})


def sale_view(request):
    if request.method == "POST":
        form_order = OrderForm(request.GET)
        form_orderline = LineForm(request.POST)
        if form_order.is_valid() and form_orderline.is_valid():

            orderline = form_orderline.save(commit=False)
            orderline.order_line_id = form_order.order_number
            orderline.order_number = 1
            orderline.unit = "ea"
            orderline.save()
    else:
        form_order = OrderForm(request.GET)
        form_orderline = LineForm()
    return render(request, 'order/Sales/sale_view.html', {'form_order': form_order, 'form_orderline': form_orderline})


