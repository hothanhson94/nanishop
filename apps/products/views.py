from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from .models import Category, Product, Brand, Feature, ProductFeature, Review
from apps.orders.models import Order, OrderItem, ShippingAddress
from apps.customers.models import Customer
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from .forms import ProductFilterForm, ReviewForm
from django.db.models import Q
from django.core.paginator import Paginator
import random
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

def home(request):
    categories = Category.objects.all()
    products_by_category = {category.slug: Product.objects.filter(category=category, new=True) for category in categories}
    products_by_top_selling = {category.slug: Product.objects.filter(category=category, top_selling=True) for category in categories}

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, is_ordered=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'order.get_total_money': 0, 'order.get_cart_items': 0}

    context={
        'products_by_category': products_by_category,
        'products_by_top_selling': products_by_top_selling,
        'categories': categories,
        'items': items,
        'order': order,
    }
    return render(request, 'index.html', context)

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    brands = Brand.objects.all()
    form = ProductFilterForm(request.GET)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, is_ordered=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'order.get_total_money': 0, 'order.get_cart_items': 0}

    top_selling_products = list(products.filter(top_selling=True))
    if len(top_selling_products) > 5:
        top_selling_products = random.sample(top_selling_products, 5)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if form.is_valid():
        category_filter = form.cleaned_data.get('category')
        brand_filter = form.cleaned_data.get('brand')

        if category_filter:
            products = products.filter(category__in=category_filter)

        if brand_filter:
            products = products.filter(brand__in=brand_filter)

        if form.cleaned_data.get('min_price') is not None:
            products = products.filter(price__gte=form.cleaned_data['min_price'])
        if form.cleaned_data.get('max_price') is not None:
            products = products.filter(price__lte=form.cleaned_data['max_price'])

        if form.cleaned_data.get('sort_by') == 'price_asc':
            products = products.order_by('price')
        elif form.cleaned_data.get('sort_by') == 'price_desc':
            products = products.order_by('-price')
        else:
            products = products.order_by('id')  # Default sorting

    else:
        products = products.order_by('id')  # Default sorting if form is not valid

    items_per_page = form.cleaned_data.get('items_per_page')
    if items_per_page and items_per_page.isdigit():
        items_per_page = int(items_per_page)
    else:
        items_per_page = 10

    paginator = Paginator(products, items_per_page)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    brands_with_counts = []
    for brand in brands:
        brand.product_count = brand.products.filter(available=True).count()
        brands_with_counts.append(brand)

    no_products_found = not page_obj.object_list.exists()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        products_html = render_to_string('products/product_list_content.html', {
            'page_obj': page_obj,
            'no_products_found': no_products_found
        }, request=request)
        pagination_html = render_to_string('products/pagination.html', {
            'page_obj': page_obj,
            'request': request,
        }, request=request)
        return JsonResponse({
            'products_html': products_html,
            'pagination_html': pagination_html,
            'start_index': page_obj.start_index(),
            'end_index': page_obj.end_index(),
            'total_count': paginator.count,
        })

    context = {
        'form': form,
        'categories': categories,
        'brands': brands_with_counts,
        'category': category,
        'products': products,
        'page_obj': page_obj,
        'no_products_found': no_products_found,
        'top_selling_products': top_selling_products,
        'request': request,
        'items': items,
        'order': order,
    }
    return render(request, 'products/product_list.html', context)

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.customer = request.user.customer
            review.save()
            messages.success(request, 'Đánh giá của bạn đã được thêm!')
            return redirect('products:product_detail', product_slug=product.slug)
    else:
        form = ReviewForm()
    context = {
        'form': form,
        'product': product
    }
    return render(request, 'products/add_review.html', context)

def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    reviews = product.reviews.all()
    images = product.images.all()
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, is_ordered=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'order.get_total_money': 0, 'order.get_cart_items': 0}

    # Lấy danh sách sản phẩm tương tự
    related_products = Product.objects.filter(
        category=product.category,
        price__gte=product.price - 5000000,
        price__lte=product.price + 5000000,
        available=True
    ).exclude(id=product.id)

    product_features = ProductFeature.objects.filter(product=product)
    feature_ids = [pf.feature.id for pf in product_features]

    if feature_ids:
        related_products = related_products.filter(product_features__feature__in=feature_ids).distinct()

    context = {
        'product': product,
        'reviews': reviews,
        'order': order,
        'items': items,
        'images': images,
        'related_products': related_products,  # Thêm danh sách sản phẩm tương tự vào context
    }

    return render(request, 'products/product_detail.html', context)

def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, available=True)
    features = Feature.objects.filter(category=category)
    brands = Brand.objects.filter(products__category=category).distinct()
    categories = Category.objects.all()

    brand_id = request.GET.get('brand')
    feature_id = request.GET.get('feature')
    sort_by = request.GET.get('sort_by')
    new_only = request.GET.get('new') == 'true'
    promotion_only = request.GET.get('promotion') == 'true'

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, is_ordered=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'order.get_total_money': 0, 'order.get_cart_items': 0}

    # Lọc sản phẩm theo thương hiệu nếu có
    if brand_id:
        products = products.filter(brand_id=brand_id)

    # Lọc sản phẩm theo tính năng nếu có
    if feature_id:
        products = products.filter(product_features__feature_id=feature_id)

    # Lọc sản phẩm mới nếu được yêu cầu
    if new_only:
        products = products.filter(new=True)

    # Lọc sản phẩm giảm giá nếu được yêu cầu
    if promotion_only:
        products = products.filter(promotion=True)

    # Sắp xếp sản phẩm
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('id')  # Default sorting

    # Phân trang
    paginator = Paginator(products, 12)  # 12 sản phẩm mỗi trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    remaining_products_count = max(0, paginator.count - (page_obj.number * 12))

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        products_html = render_to_string('products/category_detail_content.html', {
            'page_obj': page_obj,
            'category': category,
            'no_products_found': not page_obj.object_list.exists()
        }, request=request)
        return JsonResponse({
            'products_html': products_html,
            'remaining_products_count': remaining_products_count
        })

    context = {
        'category': category,
        'products': products,
        'page_obj': page_obj,
        'brands': brands,
        'items': items,
        'order': order,
        'categories': categories,
        'features': features,
        'remaining_products_count': remaining_products_count
    }
    return render(request, 'products/category_detail.html', context)

def product_search(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(brand__name__icontains=query),
            available=True
        )
    else:
        products = Product.objects.none()
    
    paginator = Paginator(products, 12)  # 12 sản phẩm mỗi trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': products,
        'query': query,
        'page_obj': page_obj
    }
    return render(request, 'products/search_results.html', context)