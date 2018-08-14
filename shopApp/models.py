from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField
from .managers import ItemManager, ReviewManager, CategoryManager, ProfileManager


class Profile(models.Model):
    LANGUAGES = (
        ('FI', 'Finnish'),
        ('EN', 'English'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_num = PhoneNumberField()
    language = models.CharField(max_length=2, choices=LANGUAGES)
    refunds_left =  models.DecimalField(decimal_places=2, max_digits=9, default=0)
    shopping_cart = ArrayField(models.IntegerField(default=0, unique=True) ,size=50, blank=True, default=[])   #list of product IDs
    my_lists = ArrayField(models.IntegerField(default=0, unique=True) ,size=200, blank=True, default=[])   #list of product IDs
    orders = ArrayField(models.IntegerField(default=0, unique=True) ,size=50, blank=True, default=[])   #list of product IDs
    objects = ProfileManager()

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    @property
    def name(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=200)
    icon = models.ImageField(upload_to="shopApp/static/img", default="")
    ad_1 = models.ImageField(upload_to="shopApp/static/img", default="")
    ad_2 = models.ImageField(upload_to="shopApp/static/img", default="")
    objects = CategoryManager()

    def __str__(self):
        return self.name

    @property
    def category_name(self):
        return self.name

class Item(models.Model):
    make = models.CharField(max_length=200, default="")
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=500)
    properties = ArrayField(models.CharField(default="", max_length=500),size=20, blank=True, default=[])   #list of product properties
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_column="category_name")
    image = models.ImageField(upload_to="shopApp/static/img", default="")
    price = models.DecimalField(decimal_places=2, max_digits=9)
    quantityAvailable = models.IntegerField(default=0)
    date_added = models.DateTimeField('date added')
    objects = ItemManager()

    def __str__(self):
        return self.name

    @property
    def date(self):
        return self.date_added.date

class Review(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    # --- if logged in: ---
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True, null=True)
    user_fullname = models.CharField(max_length=200, blank=True, null=True, default="") #for angularjs
    # --- if not logged in: ---
    email = models.CharField(max_length=200, blank=True, null=True)
    age = models.CharField(max_length=50, blank=True, null=True)
    nickname = models.CharField(max_length=200, blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    #------------------------
    title = models.CharField(max_length=200, default="")
    text = models.CharField(max_length=2000)
    stars = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    recommend = models.BooleanField(default=False)
    date_added = models.DateTimeField('date added')

    def __str__(self):
        return self.item.name

    @property
    def date(self):
        return self.date_added.date
