from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.db.models import Avg
from django.utils import timezone
from django.http import JsonResponse
import json
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def index(request):
    categories = Category.objects.order_by('name')
    profile = Profile.objects.get(user=request.user)
    new_items_list = Item.objects.order_by('-date_added')[:25]
    reviews = Review.objects.order_by('-date_added')[:25]                                       #AngularJS tilalle
    context = {'new_items_list': new_items_list, 'categories': categories, 'reviews': reviews, 'profile': profile}
    return render(request, 'shopApp/index.html', context)

def info(request, item_id):
    categories = Category.objects.order_by('name')
    profile = Profile.objects.get(user=request.user)
    context = {'categories': categories, 'profile': profile}
    return render(request, 'shopApp/info.html', context)

def results(request, category_name):
    categories = Category.objects.order_by('name')
    profile = Profile.objects.get(user=request.user)
    items = Item.objects.filter(category__name=category_name)
    category = Category.objects.get(name=category_name)
    context = {'items': items, 'categories': categories, 'category': category, 'profile': profile}
    return render(request, 'shopApp/results.html', context)

def checkout(request, user_id):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)

        # Add the actual item objects in the 'cart' array
        cart = []
        for item_id in profile.shopping_cart:
            for item in Item.objects.all():
                if item_id == item.id:
                    cart.insert(0, item)

        # If user has not yet an order object instance, create new
        if not Order.objects.filter(user=request.user):
            # Get the total price of cart contents
            order.total_price = 0
            for item in cart:
                total_price += item.price
            order = Order.objects.create(items=profile.shopping_cart, user=request.user, full_name=request.user.get_full_name(), street_address=profile.street_address, zip_code=profile.zip_code, city=profile.city, phone_num=profile.phone_num, email=request.user.email, total_price=total_price)
            order.save()

        # If user already has an order instance, get it
        else:
            order = Order.objects.get(user=request.user)
            order.items = profile.shopping_cart
            order.total_price = 0
            for item in cart:
                order.total_price += item.price
            order.save()

        context = {'profile': profile, 'cart': cart, 'order': order}
    #if not request.user.is_authenticated:
    #    order = BORDER BORDER
        return render(request, 'shopApp/checkout.html', context)

def write(request, item_id):
    categories = Category.objects.order_by('name')
    profile = Profile.objects.get(user=request.user)
    item = Item.objects.get(pk=item_id)
    context = {'categories': categories, 'item': item, 'profile': profile}
    return render(request, 'shopApp/write_review.html', context)

def account(request):
    categories = Category.objects.order_by('name')
    profile = Profile.objects.get(user=request.user)
    orders_list = []
    for item_id in profile.orders:
        for item in Item.objects.all():
            if item_id == item.id:
                orders_list.insert(0, item)
    context = {'categories': categories, 'orders_list': orders_list, 'profile': profile}
    return render(request, 'shopApp/account.html', context)

def login_view(request):
    if not request.user.is_authenticated:
        categories = Category.objects.order_by('name')
        profile = Profile.objects.get(user=request.user)
        context = {'categories': categories, 'profile': profile}
        return render(request, 'shopApp/login.html', context)
    else:
        return redirect("/")

def signup(request):
    categories = Category.objects.order_by('name')
    profile = Profile.objects.get(user=request.user)
    context = {'categories': categories, 'profile': profile}
    return render(request, 'shopApp/signup.html', context)


#---------------- ACTIONS ---------------

#----- CHECKOUT ----

def addToCart(request):
    if request.method == 'POST':
        id = request.body.decode('utf-8')
        profile = Profile.objects.get(user=request.user)
        profile.shopping_cart.append(id)
        profile.save()
        return JsonResponse({'cart': profile.shopping_cart})



def addContacts(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        street_address = data['street_address']
        zip_code = data['zip_code']
        city = data['city']
        phone_num = data['phone_num']
        email = data['email']
        profile = Profile.objects.get(user=request.user)
        profile.street_address = street_address
        profile.zip_code = zip_code
        profile.city = city
        profile.phone_num = phone_num
        profile.email = email
        profile.save()
        order = Order.objects.get(user=request.user)
        order.street_address = street_address
        order.zip_code = zip_code
        order.city = city
        order.phone_num = phone_num
        order.email = email
        order.save()
        # Turha?
        return JsonResponse({
            'street_address': order.street_address,
            'zip_code': order.zip_code,
            'city': order.city,
            'phone_num': str(order.phone_num),
            'email': order.email
        })

def addDelivery(request):
    if request.method == 'POST':
        delivery = request.body.decode('utf-8')
        order = Order.objects.get(user=request.user)
        order.delivery_method = delivery
        order.save()
        return JsonResponse({'delivery_method': order.delivery_method})

def addPayment(request):
    if request.method == 'POST':
        payment = request.body.decode('utf-8')
        order = Order.objects.get(user=request.user)
        order.payment_method = payment
        order.save()
        return JsonResponse({'payment_method': order.payment_method})

def confirmOrder(request):
    profile = Profile.objects.get(user=request.user)
    order = Order.objects.get(user=request.user)
    order.confirmed = True
    orders_list = []
    for item_id in profile.shopping_cart:
        for item in Item.objects.all():
            if item_id == item.id:
                orders_list.insert(0, item)


    html_message = loader.render_to_string(
    "../templates/shopApp/email_confirm.html",
    {
        'user': request.user,
        'profile': profile,
        'orders_list': orders_list
    }
    ).strip()

    subject = 'Thank you for your order!'

    message = EmailMultiAlternatives(subject, html_message, settings.EMAIL_HOST_USER, ['niklas.byggmastar@gmail.com'])
    message.content_subtype = 'html'
    message.mixed_subtype = 'related'
    for item in orders_list:
        image = MIMEImage(item.image.read())
        image.add_header('Content-ID', '<{}>'.format(item.image_filename))
        message.attach(image)

    message.send()



#    send_mail(subject, "", settings.EMAIL_HOST_USER, ['niklas.byggmastar@gmail.com'], fail_silently=False, html_message=html_message)
    return redirect("/?checkyallmail")

#----- /CHECKOUT ----


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
            review = Review.objects.create(item=item, email=email, age=age, nickname=nickname, gender=gender, title=title, text=review_text, stars=stars, recommend=recommend, date_added=timezone.now())
        else:
            user_fullname = request.user.first_name + " " + request.user.last_name
            review = Review.objects.create(item=item, user=request.user, user_fullname=user_fullname, title=title, text=review_text, stars=stars, recommend=recommend, date_added=timezone.now())
        review.save()
        messages.success(request, 'Review posted successfully!', extra_tags="alert-success")
        return redirect("/%3F"+str(item_id))



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
