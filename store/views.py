from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from django.http import JsonResponse
from cart.cart import Cart

def add_to_cart(request, pk):
    """
    Adds a product to the cart.
    """
    product = get_object_or_404(Product, pk=pk)
    cart = Cart(request)
    cart.add(product, 1)  # Ensure this method works as expected
    return JsonResponse({'message': 'Product added to cart'})

def cart_summary(request):
    """
    Displays the summary of the cart.
    """
    cart = Cart(request)
    total_items = cart.get_total_items()
    return render(request, 'cart/cart_summary.html', {'cart': cart, 'total_items': total_items})

def cart_add(request):
    """
    Adds a product to the cart via POST request.
    """
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        cart = Cart(request)
        cart.add(product, quantity)
        response = {
            'message': 'Product added to cart successfully',
            'total_items': cart.get_total_items()
        }
        return JsonResponse(response)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def cart_delete(request):
    """
    Removes a product from the cart via POST request.
    """
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        cart = Cart(request)
        cart.remove(product)
        response = {
            'message': 'Product removed from cart successfully',
            'total_items': cart.get_total_items()
        }
        return JsonResponse(response)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def cart_update(request):
    """
    Updates the quantity of a product in the cart via POST request.
    """
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        cart = Cart(request)
        cart.add(product, quantity)
        response = {
            'message': 'Cart updated successfully',
            'total_items': cart.get_total_items()
        }
        return JsonResponse(response)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def home(request):
    """
    Displays the home page with a list of all products.
    """
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    """
    Displays the about page.
    """
    return render(request, 'about.html', {})

def category(request, foo):
    """
    Displays products for a specific category.
    """
    category_name = foo.replace('-', ' ')
    try:
        category = Category.objects.get(name=category_name)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'category': category, 'products': products})
    except Category.DoesNotExist:
        messages.error(request, "This category does not exist.")
        return redirect('home')

def product_detail(request, pk):
    """
    Displays details of a single product.
    """
    product = get_object_or_404(Product, id=pk)
    return render(request, 'product.html', {'product': product})

def login_user(request):
    """
    Handles user login.
    """
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in successfully.")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    """
    Handles user logout.
    """
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')

def register_user(request):
    """
    Handles user registration.
    """
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Your account has been created and you are now logged in!")
                return redirect('home')
            else:
                messages.error(request, "There was an error during authentication. Please try again.")
        else:
            messages.error(request, "Please correct the errors below and try again.")
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})
