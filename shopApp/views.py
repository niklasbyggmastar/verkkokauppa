from django.shortcuts import render, redirect
from .models import Item
from .models import Category
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

def index(request):
    categories = Category.objects.all()
    new_items_list = Item.objects.order_by('-date_added')[:25]
    context = {'new_items_list': new_items_list, 'categories': categories}
    return render(request, 'shopApp/index.html', context)

def info(request, item_id):
    categories = Category.objects.all()
    item = Item.objects.get(pk=item_id)
    context = {'item': item, 'categories': categories}
    return render(request, 'shopApp/info.html', context)

def results(request, category_name):
    categories = Category.objects.all()
    items = Item.objects.filter(category__name=category_name)
    category = Category.objects.get(name=category_name)
    context = {'items': items, 'categories': categories, 'category': category}
    return render(request, 'shopApp/results.html', context)

def buy(request, item_id):
    categories = Category.objects.all()
    context = {'item_id': item_id, 'categories': categories}
    return render(request, 'shopApp/buy.html', context)

def account(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'shopApp/account.html', context)

def login_view(request):
    if not request.user.is_authenticated:
        categories = Category.objects.all()
        context = {'categories': categories}
        return render(request, 'shopApp/login.html', context)
    else:
        return redirect("/")

def signup(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'shopApp/signup.html', context)


#---------------- ACTIONS ---------------

def check_email(request):
    if request.method == 'POST':
        email_exists = False
        email = request.POST['email']
        if not User.objects.filter(email=email).exists(): #no email exists
            messages.warning(request, 'There is no account with the given email address.', extra_tags='alert-danger')
            return redirect("login_view")
        else:                                            #email exists
            return redirect("../login_view?email="+email)


def login_action(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!', extra_tags="alert-success")
            return redirect("../")
        else:
            messages.warning(request, 'Email and password do not match.', extra_tags='alert-danger')
            return redirect("/login_view?email="+email)


def logout_action(request):
    logout(request)
    messages.success(request, 'Logout successful!', extra_tags="alert-success")
    return redirect("../")
