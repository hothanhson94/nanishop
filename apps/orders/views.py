from django.shortcuts import render

# Create your views here.
def order_list(request):
    return render(request, 'orders/order_list.html')

def order_detail(request):
    return render(request, 'orders/order_detail.html')