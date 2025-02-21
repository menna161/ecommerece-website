from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.db.models import Q

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})

def home(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    products = Product.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()
    return render(request, 'shop/home.html', {'products': products, 'categories': categories})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']  # Set the email as the username
            user.is_active = True  # Activate account immediately
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  # Log the user in immediately after registration
            return redirect('login')  # Redirect to login page
    else:
        form = RegistrationForm()
    return render(request, 'shop/register.html', {'form': form})

def registration_complete(request):
    return render(request, 'shop/registration_complete.html')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')  # Redirect to home page
                else:
                    messages.error(request, 'Account is not active. Please contact support.')
            else:
                messages.error(request, 'Invalid email or password')
        else:
            print("Login form is not valid")  # Debug statement
            print(form.errors)  # Print form errors
            messages.error(request, 'Invalid email or password')
    else:
        form = LoginForm()
    return render(request, 'shop/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to home page