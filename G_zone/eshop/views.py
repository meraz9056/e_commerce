from django.http import HttpResponse
from django.shortcuts import redirect, render

from eshop.models import Category,Product,Slider,Contact,Order
from django.contrib.auth import authenticate
from .forms import UserCreateForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from cart.cart import Cart
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import reverse
from django.views.generic import TemplateView, FormView
from .forms import ContactForm
from django.contrib.auth.models import User
from decimal import Decimal

# Create your views here.
def home(request):
    category = Category.objects.all()
    slider = Slider.objects.all().order_by('-id')
    
    categoryID = request.GET.get('category')
    if categoryID:
        product = Product.objects.filter(sub_category = categoryID).order_by('-id')
    else:
        product = Product.objects.all()


    context = {
        'category':category,
        'product':product,
        'slider':slider,

    }
    return render(request, "home.html",context)


def signup(request):
    if request.method == 'POST':
       form = UserCreateForm(request.POST)
       if form.is_valid():
        new_user = form.save()
        new_user = authenticate(
           username = form.cleaned_data['username'],
           password = form.cleaned_data['password1'],
        )
        
        return redirect('login')
    
    else:
       form = UserCreateForm()
    context = {
       
       'form':form,
    }
    return render(request, 'user/signUp.html',context)

def login1(request):
      if request.method == 'POST':
 
        # AuthenticationForm_can_also_be_used__
 
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' welcome {username} !!')
            return redirect('home')
        else:
            messages.info(request, f'account done not exit plz sign in')
        
      return render(request, 'registration/login.html')

@login_required(login_url="/accounts/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="/accounts/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')



def contact_view(request):
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                form.save() # This saves the data to the database
                return redirect('contact_success') # Redirect to a success page
        else:
            form = ContactForm()
        return render(request, 'contact.html', {'form': form})

def contact_success(request):
        return render(request, 'success.html')



def checkout(request):

    if request.method == "POST":
       phone = request.POST.get('mobile')
       address = request.POST.get('address')
       cart = request.session.get('cart')
       uid = request.session.get('_auth_user_id')
       user = User.objects.get(pk = uid)

       print(phone,address,cart)
       for i in cart:
           print(i)
           a = cart[i]['price']
           b = (cart[i]['quantity'])
           total = a*b

           order = Order(
               user = user,
               product = cart[i]['name'],
               price  = cart[i]['price'],
               quantity  = cart[i]['quantity'],
               total = total, 
               image  = cart[i]['image'],
               phone = phone,
               address = address,
           )
           order.save()
           request.session['cart'] = {}
       return redirect('home')
    return HttpResponse("This is checkout page")