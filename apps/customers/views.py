from django.shortcuts import render

# Create your views here.
def login_view(request):
    return render(request, 'customers/login.html')

def register_view(request):
    return render(request, 'customers/register.html')