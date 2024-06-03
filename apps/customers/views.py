from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from apps.products.models import Product

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Tài khoản của bạn đã được tạo! Bạn có thể đăng nhập ngay bây giờ.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'customers/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Hồ sơ của bạn đã được cập nhật!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'customers/profile.html', context)

@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    profile = request.user.profile
    if product in profile.favorite_products.all():
        profile.favorite_products.remove(product)
        messages.success(request, f'Sản phẩm đã được xóa khỏi danh sách yêu thích.')
    else:
        profile.favorite_products.add(product)
        messages.success(request, f'Sản phẩm đã được thêm vào danh sách yêu thích.')
    return redirect('product_detail', product_id=product.id)

@login_required
def favorite_list(request):
    profile = request.user.profile
    favorites = profile.favorite_products.all()
    return render(request, 'customers/favorite_list.html', {'favorites': favorites})
