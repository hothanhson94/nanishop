from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order
from apps.products.models import Product
from django.contrib import messages

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True)
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order, created = Order.objects.get_or_create(user=request.user, product=product, is_ordered=False)
    if created:
        order.quantity = 1
        messages.success(request, f'Sản phẩm đã được thêm vào giỏ hàng.')
    else:
        order.quantity += 1
        messages.success(request, f'Số lượng sản phẩm đã được cập nhật.')
    order.save()
    return redirect('cart')

def cart(request):
    context = {}
    return render(request, 'orders/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'orders/checkout.html', context)