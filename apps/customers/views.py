from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Customer, NewsletterSubscription
from apps.products.models import Product
from apps.orders.models import Order, OrderItem
from .forms import NewsletterForm
import datetime
import re

def register(request):
    errors = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        terms = request.POST.get('terms')

        if not terms:
            errors['terms'] = 'Bạn phải đồng ý với các điều khoản và điều kiện!'
        elif re.search(r'[^a-zA-Z0-9_]', username):
            errors['username'] = 'Tên đăng nhập không được chứa ký tự đặc biệt!'
        elif password1 != password2:
            errors['password2'] = 'Mật khẩu không khớp!'
        elif User.objects.filter(username=username).exists():
            errors['username'] = 'Username đã tồn tại!'
        elif User.objects.filter(email=email).exists():
            errors['email'] = 'Email đã được sử dụng!'
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            Customer.objects.create(user=user, name=name, email=email, gender=gender, address=address)
            messages.success(request, 'Đăng ký thành công. Vui lòng đăng nhập!')
            return redirect('login')

    context = {
        'errors': errors
    }
    return render(request, 'customers/register.html', context)

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không chính xác!')
    return render(request, 'customers/login.html')

def custom_logout(request):
    logout(request)
    return redirect('index')

@login_required
def profile(request):
    customer = request.user.customer
    orders = Order.objects.filter(customer=customer).order_by('-date_ordered')
    favorites = customer.favorite_products.all()

    if request.method == 'POST':
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        birth_date = request.POST.get('birth_date')
        gender = request.POST.get('gender')
        
        # Validate birth_date
        if not birth_date:
            messages.error(request, 'Vui lòng nhập ngày tháng năm sinh!')
            return redirect('profile')
        try:
            datetime.datetime.strptime(birth_date, '%Y-%m-%d')
        except ValueError:
            messages.error(request, 'Định dạng ngày tháng năm sinh không hợp lệ. Định dạng hợp lệ là YYYY-MM-DD.')
            return redirect('profile')

        customer.address = address
        customer.phone_number = phone_number
        customer.birth_date = birth_date
        customer.gender = gender
        customer.save()
        messages.success(request, 'Hồ sơ của bạn đã được cập nhật!')
        return redirect('profile')

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, is_ordered=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'order.get_total_money': 0, 'order.get_cart_items': 0}

    context = {
        'customer': customer,
        'items': items,
        'order': order,
        'orders': orders,
        'favorites': favorites,
    }
    return render(request, 'customers/profile.html', context)

@login_required
def favorite_list(request):
    customer = request.user.customer
    favorites = customer.favorite_products.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, is_ordered=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'order.get_total_money': 0, 'order.get_cart_items': 0}

    context = {
        'items': items,
        'order': order,
        'favorites': favorites,
    }
    return render(request, 'customers/favorite_list.html', context)

@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    customer = request.user.customer
    if product in customer.favorite_products.all():
        customer.favorite_products.remove(product)
        messages.success(request, 'Sản phẩm đã được xóa khỏi danh sách yêu thích.')
    else:
        customer.favorite_products.add(product)
        messages.success(request, 'Sản phẩm đã được thêm vào danh sách yêu thích.')
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def edit_profile(request):
    customer = request.user.customer
    if request.method == 'POST':
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        birth_date = request.POST.get('birth_date')
        gender = request.POST.get('gender')

        # Validate birth_date
        if not birth_date:
            messages.error(request, 'Vui lòng nhập ngày tháng năm sinh!')
            return redirect('profile')
        try:
            datetime.datetime.strptime(birth_date, '%Y-%m-%d')
        except ValueError:
            messages.error(request, 'Định dạng ngày tháng năm sinh không hợp lệ. Định dạng hợp lệ là YYYY-MM-DD.')
            return redirect('profile')

        customer.address = address
        customer.phone_number = phone_number
        customer.birth_date = birth_date
        customer.gender = gender
        customer.save()
        messages.success(request, 'Hồ sơ của bạn đã được cập nhật!')
        return redirect('profile')

    context = {
        'customer': customer,
    }
    return render(request, 'customers/edit_profile.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Quan trọng để giữ người dùng đăng nhập
            messages.success(request, 'Mật khẩu của bạn đã được thay đổi thành công!')
            return redirect('profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'customers/profile.html', {'form': form})

def newsletter_signup(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bạn đã đăng ký nhận thông tin khuyến mãi thành công. Thank you!')
        else:
            messages.error(request, 'Email này đã được đăng ký hoặc không hợp lệ.')
    return redirect('index')