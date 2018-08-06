from django.shortcuts import render, redirect
from .models import Item, Category, Review
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.db.models import Avg
from django.utils import timezone


def index(request):
    categories = Category.objects.order_by('name')
    new_items_list = Item.objects.order_by('-date_added')[:25]
    reviews = Review.objects.order_by('-date_added')[:25]
    context = {'new_items_list': new_items_list, 'categories': categories, 'reviews': reviews}
    return render(request, 'shopApp/index.html', context)

def info(request, item_id):
    categories = Category.objects.order_by('name')
    item = Item.objects.get(pk=item_id)
    reviews = Review.objects.filter(item=item)
    remaining = 5
    if reviews:
        recommended = round((len(reviews.filter(recommend=True)) / len(reviews)) * 100)
        average_stars = round(list(reviews.aggregate(Avg('stars')).values())[0]) # 1 decimal place
        loop_times = range(0, round(average_stars))
        remaining = range(average_stars, 5)
        context = {'item': item, 'categories': categories, 'average_stars': average_stars, 'reviews': reviews, 'recommended': recommended, 'loop_times': loop_times, 'remaining': remaining}
    else:
        context = {'item': item, 'categories': categories, 'reviews': reviews}
    return render(request, 'shopApp/info.html', context)

def results(request, category_name):
    categories = Category.objects.order_by('name')
    items = Item.objects.filter(category__name=category_name)
    category = Category.objects.get(name=category_name)
    context = {'items': items, 'categories': categories, 'category': category}
    return render(request, 'shopApp/results.html', context)

def buy(request, item_id):
    categories = Category.objects.order_by('name')
    context = {'item_id': item_id, 'categories': categories}
    return render(request, 'shopApp/buy.html', context)

def write(request, item_id):
    categories = Category.objects.order_by('name')
    item = Item.objects.get(pk=item_id)
    context = {'categories': categories, 'item': item}
    return render(request, 'shopApp/write_review.html', context)

def account(request):
    categories = Category.objects.order_by('name')
    orders_list = []
    for item_id in request.user.profile.orders:
        for item in Item.objects.all():
            if item_id == item.id:
                orders_list.insert(0, item)
    context = {'categories': categories, 'orders_list': orders_list}
    return render(request, 'shopApp/account.html', context)

def login_view(request):
    if not request.user.is_authenticated:
        categories = Category.objects.order_by('name')
        context = {'categories': categories}
        return render(request, 'shopApp/login.html', context)
    else:
        return redirect("/")

def signup(request):
    categories = Category.objects.order_by('name')
    context = {'categories': categories}
    return render(request, 'shopApp/signup.html', context)


#---------------- ACTIONS ---------------

def post_review(request, item_id):
    if request.method == 'POST':
        item = Item.objects.get(pk=item_id)
        stars = request.POST['stars']
        recommend = request.POST.get('recommend', False)
        title = request.POST['title']
        review_text = request.POST['review_text']
        if not request.user.is_authenticated:
            email = request.POST['email']
            age = request.POST['age']
            nickname = request.POST['nickname']
            gender = request.POST['gender']
        review = Review.objects.create(item=item, user=request.user, title=title, text=review_text, stars=stars, recommend=recommend, date_added=timezone.now())
        review.save()
        return redirect("/"+str(item_id)+"?review=added")


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
