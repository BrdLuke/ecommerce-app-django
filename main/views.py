from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from main.models import Product, Payment

# Create your views here

def home(request):
    # if request.method == 'POST':
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     # Authenticate
    #     user = authenticate(request, username=username, password=password)
    #     if user is not None:
    #         login(request, user)
    #         messages.success(request, "You have been logged in")
    #         return redirect('home') # Render to home page
    #     else:
    #         messages.error(request, "Username or password wrong. Please try again")
    return render(request, 'home.html', {})


def find_us_view(request):
    return render(request, 'find_us.html', {})


def contact_us_view(request):
    return render(request, 'contact_us.html', {})


def about_us_view(request):
    return render(request, 'about_us.html', {})


def login_user(request):
    if request.method == 'POST':
        username    = request.POST['username']
        password    = request.POST['password']
        # Authenticate
        user        = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in")
            return redirect('home') # Render to home page
        else:
            messages.error(request, "Username or password wrong. Please try again")

    return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('home') # Render to home page


def register_user(request):
    if request.method == 'POST':
        username            = request.POST['username']
        email               = request.POST['email']
        password            = request.POST['password']
        confirm_password    = request.POST['confirm_password']

        if(password != confirm_password):
            messages.error(request, "Seems that the passwords are different. Try again!")
            return redirect('register') # Render to register page
        
        if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
            messages.error(request, "Username or email already exists. Please choose a different ones.")
            return redirect('register')  # Re-render the register page with an error message

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()

        messages.success(request, "Your account has been successfully created!\nSign in with your credentials.")
        return redirect('login')  # Render to login page

    return render(request, 'registration.html', {})


def details_user(request, pk):
    if request.user.is_authenticated:
        user_detail = User.objects.get(id = pk)
        cart_products = Product.objects.filter(cart = True)
        cart_count = cart_products.count()
        total_price = 0

        for product in cart_products:
            quantity = request.POST.get('quantity_{}'.format(product.id))
            if quantity:
                product.product_quantity = quantity
                product.save()

            if product.product_quantity is not None:
                total_price += (float(product.product_price) * float(product.product_quantity))
        
        return render(request, 'user_details.html', {'user_detail': user_detail, 'cart_count': cart_count, 'cart_products': cart_products, 'total_price': total_price})
    else:
        messages.error(request, "Username or email already exists. Please choose a different ones.")
        return redirect('home')  # Render to the home page with an error message
    

def update_user_details(request):
    if request.method == 'POST':
        user                = request.user
        user.first_name     = request.POST['first_name']
        user.last_name      = request.POST['last_name']
        user.username       = request.POST['username']
        user.email          = request.POST['email']
        new_password        = request.POST['password']

        if new_password:
            user.set_password(new_password)
            user.save()
            messages.success(request, "You changed your data! Please sign in with your new credentials")
            return redirect('login') # Render to login page
    
    return render(request, 'update_form_user.html')


def products_list(request):
    products = Product.objects.order_by('product_category')

    if not products:
        messages.error(request, "At this moment there aren't products available ...")

    categories = set(products.values_list('product_category', flat=True))
    all_products = {}

    for category in categories:
        category_products       = products.filter(product_category = category)
        all_products[category]  = category_products

    context = {'all_products': all_products}
    return render(request, 'products.html', context)


def details_product(request, product_name):
    product_details = Product.objects.get(product_name = product_name)

    return render(request, 'product_details.html', {'product_details': product_details})


def checkout(request, product_name):
    if request.user.is_authenticated:
        if request.method == 'POST':
            email               = request.POST['email']
            tel                 = request.POST['tel']
            date                = request.POST['date']
            cvc                 = request.POST['cvc']
            name_card           = request.POST['name_card']
            continents          = request.POST['continents']
            zip                 = request.POST['zip']
            #product             = request.GET['product_name']   
            #TODO: catch the product name so in the model 'Payment' I can see what product the client bought

            checkout_fields     = Payment(email=email, tel=tel, date=date, cvc=cvc, name_card=name_card, continents=continents, zip=zip)
            checkout_fields.save()
            return render(request, 'checkout_status.html', {})
        else:
            product_details     = Product.objects.get(product_name = product_name)
            return render       (request, 'checkout.html', {'product_details': product_details})
    else:
        messages.error          (request, "You must be logged in for buying. Sign in if you have an account or sign up!")
        return redirect         ('home')
    

def custom_404(request, exception):
    return render(request, '404.html', status=404)


def add_to_cart(request, pk):
    product = get_object_or_404(Product, id = pk)
    if product.cart == True:
        messages.info(request, "This product is already in your cart!")
    else:
        messages.info(request, "Product added to your cart!")
    product.cart = True
    product.save()
    return redirect(request.META['HTTP_REFERER'])


def delete_from_cart(request, pk):
    product = get_object_or_404(Product, id = pk)
    if product.cart == True:
        product.cart = False
        product.product_quantity = None
        product.save()
    
    messages.info(request, "Product deleted from your cart successfully!")
    return redirect(request.META['HTTP_REFERER'])


def checkout_cart(request, pk):
    if request.user.is_authenticated:
        user_id     = User.objects.get(id = pk)
        
        cart_products = Product.objects.filter(cart = True)
        total_price = 0

        for product in cart_products:
            if product.product_quantity is not None:
                total_price += (float(product.product_price) * float(product.product_quantity))

        return render(request, 'user_details_checkout_cart.html', {'user_id': user_id, 'cart_products': cart_products, 'total_price': total_price})
    
    if request.method == 'POST':
        email               = request.POST['email']
        tel                 = request.POST['tel']
        date                = request.POST['date']
        cvc                 = request.POST['cvc']
        name_card           = request.POST['name_card']
        continents          = request.POST['continents']
        zip                 = request.POST['zip']
        #product             = request.GET['product_name']   
        #TODO: catch the product name so in the model 'Payment' I can see what product the client bought

        checkout_fields     = Payment(email=email, tel=tel, date=date, cvc=cvc, name_card=name_card, continents=continents, zip=zip)
        checkout_fields.save()
        return render(request, 'checkout_status.html', {})
    else:
        user_details          = User.objects.get(id = pk)
        return redirect       ('user_details', {'user_details': user_details})