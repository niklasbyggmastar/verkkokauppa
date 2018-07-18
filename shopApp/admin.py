from django.contrib import admin

from .models import Item
from .models import Review
from .models import Category

admin.site.register(Item)
admin.site.register(Review)
admin.site.register(Category)
