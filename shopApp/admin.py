from django.contrib import admin

from .models import Item, Review, Category, Profile, Order

admin.site.register(Item)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Order)
