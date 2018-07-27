from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField


class Profile(models.Model):
    LANGUAGES = (
        ('FI', 'Finnish'),
        ('EN', 'English'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_num = PhoneNumberField()
    language = models.CharField(max_length=2, choices=LANGUAGES)
    refunds_left =  models.DecimalField(decimal_places=2, max_digits=9, default=0)
    orders = ArrayField(models.IntegerField(default=0, unique=True) ,size=50, blank=True, default=[])   #list of product IDs

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Category(models.Model):
    name = models.CharField(max_length=200)
    icon = models.ImageField(upload_to="shopApp/static/img", default="")
    ad_1 = models.ImageField(upload_to="shopApp/static/img", default="")
    ad_2 = models.ImageField(upload_to="shopApp/static/img", default="")

    def __str__(self):
        return self.name

class Item(models.Model):
    make = models.CharField(max_length=200, default="")
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=5000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="shopApp/static/img", default="")
    price = models.DecimalField(decimal_places=2, max_digits=9)
    quantityAvailable = models.IntegerField(default=0)
    date_added = models.DateTimeField('date added')

    def __str__(self):
        return self.name

class Review(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="")
    text = models.CharField(max_length=500)
    stars = models.PositiveIntegerField(validators=[MinValueValidator(0)], default=0)

#------------------------------------------------------------------------------------

#class MyUserManager(BaseUserManager):
#    """
#    A custom user manager to deal with emails as unique identifiers for auth
#    instead of usernames. The default that's used is "UserManager"
#    """
#    def _create_user(self, email, password, **extra_fields):
#        """
#        Creates and saves a User with the given email and password.
#        """
#        if not email:
#            raise ValueError('The Email must be set')
#        email = self.normalize_email(email)
#        user = self.model(email=email, **extra_fields)
#        user.set_password(password)
#        user.save()
#        return user

#    def create_superuser(self, email, password, **extra_fields):
#        extra_fields.setdefault('is_staff', True)
#        extra_fields.setdefault('is_superuser', True)
#        extra_fields.setdefault('is_active', True)

#        if extra_fields.get('is_staff') is not True:
#            raise ValueError('Superuser must have is_staff=True.')
#        if extra_fields.get('is_superuser') is not True:
#            raise ValueError('Superuser must have is_superuser=True.')
#        return self._create_user(email, password, **extra_fields)


#class User(AbstractBaseUser, PermissionsMixin):
#    email = models.EmailField(unique=True, null=True)
#    is_staff = models.BooleanField(
#        _('staff status'),
#        default=False,
#        help_text=_('Designates whether the user can log into this site.'),
#    )
#    is_active = models.BooleanField(
#        _('active'),
#        default=True,
#        help_text=_(
#            'Designates whether this user should be treated as active. '
#            'Unselect this instead of deleting accounts.'
#        ),
#    )
#    USERNAME_FIELD = 'email'
#    objects = MyUserManager()
#
#    def __str__(self):
#        return self.email
#
#    def get_full_name(self):
#        return self.email
#
#    def get_short_name(self):
#        return self.email
#
