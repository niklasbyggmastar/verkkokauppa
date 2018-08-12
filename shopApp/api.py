from tastypie.resources import ModelResource
from .models import Item, Review
from tastypie import fields
from tastypie.api import Api

class ItemResource(ModelResource):
    class Meta:
        queryset = Item.objects.all()
        resource_name = 'item'

class ReviewResource(ModelResource):
    item = fields.ForeignKey(ItemResource, 'item')
    class Meta:
        queryset = Review.objects.all()
        resource_name = 'review'

    def dehydrate(self,bundle):
        bundle.data['new_date_format'] = '10.8.2018'
        return bundle

v1_api = Api(api_name='v1')
v1_api.register(ItemResource())
v1_api.register(ReviewResource())
