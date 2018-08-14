from tastypie.resources import ModelResource
from .models import Item, Review, Profile, Category
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.api import Api

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'

class ProfileResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        queryset = Profile.objects.all()
        resource_name = 'profile'

class CategoryResource(ModelResource):
    class Meta:
        queryset = Category.objects.all()
        resource_name = 'category'

class ItemResource(ModelResource):
    category = fields.ForeignKey(CategoryResource, 'category')
    class Meta:
        queryset = Item.objects.all()
        resource_name = 'item'

class ReviewResource(ModelResource):
    item = fields.ForeignKey(ItemResource, 'item')
    class Meta:
        queryset = Review.objects.all()
        resource_name = 'review'

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(ProfileResource())
v1_api.register(CategoryResource())
v1_api.register(ItemResource())
v1_api.register(ReviewResource())
