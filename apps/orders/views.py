from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem, ShippingAddress
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
import json
from django.views.decorators.csrf import csrf_exempt
from apps.products.models import Product, Feature, ProductFeature
from django.contrib import messages

@login_required
def order_list(request):
    orders = Order.objects.filter(customer=request.user.customer, is_ordered=True)
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user.customer)
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
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, is_ordered=False)
        items = order.orderitem_set.all()
        
        # Logic để lấy ra danh sách sản phẩm gợi ý
        suggested_products = Product.objects.none()
        
        if any(item.product.category.slug in ["dien-thoai", "tablet"] for item in items):
            suggested_features = ["Ốp lưng", "Tai nghe", "Sạc, cáp", "Sạc dự phòng", "Tai nghe"]
            suggested_products = Product.objects.filter(
                Q(product_features__feature__name__in=suggested_features)
            ).distinct()
        elif any(item.product.category.slug == "laptop" for item in items):
            suggested_features = ["Bàn phím", "Chuột", "Loa"]
            suggested_products = Product.objects.filter(
                Q(product_features__feature__name__in=suggested_features)
            ).distinct()
        elif all(item.product.category.slug == "phu-kien" for item in items):
            suggested_products = Product.objects.none()
    else:
        items = []
        order = {'order.get_total_money': 0, 'order.get_cart_items': 0}
        suggested_products = Product.objects.none()
    
    context = {
        'items': items,
        'order': order,
        'suggested_products': suggested_products,  # Thêm danh sách sản phẩm gợi ý vào context
    }
    return render(request, 'orders/cart.html', context)

@csrf_exempt
def updateItem(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            productId = data['productId']
            action = data['action']
            
            customer = request.user.customer
            product = Product.objects.get(id=productId)
            order, created = Order.objects.get_or_create(customer=customer, is_ordered=False)
            orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
            
            if action == 'add':
                orderItem.quantity += 1
                orderItem.save()
            elif action == 'remove':
                orderItem.quantity -= 1
                if orderItem.quantity <= 0:
                    orderItem.delete()
                else:
                    orderItem.save()
            elif action == 'remove_all':
                orderItem.delete()
            
            response_data = {
                'productId': productId,
                'action': action,
                'cartTotalItems': order.get_cart_items,
                'cartTotalMoney': float(order.get_total_money),  # Đảm bảo trả về số thực
                'itemQuantity': orderItem.quantity if orderItem.id else 0,
                'productPrice': float(product.price_after_discount),  # Đảm bảo trả về số thực
            }
            
            return JsonResponse(response_data, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def checkout(request):
    if request.method == 'POST':
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, is_ordered=False)

        shipping_address = ShippingAddress(
            customer=customer,
            order=order,
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
        )
        shipping_address.save()

        order.payment_method = request.POST.get('payment')
        order.is_ordered = True
        order.save()

        messages.success(request, 'Thanh toán thành công! Đơn hàng của bạn đã được đặt.')
        return redirect('index')  # Chuyển hướng về trang chủ
    
    else:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, is_ordered=False)
        items = order.orderitem_set.all()
        
        context = {
            'items': items,
            'order': order,
        }
        return render(request, 'orders/checkout.html', context)