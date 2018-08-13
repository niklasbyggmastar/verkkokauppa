from django.db.models.manager import Manager
import datetime

class CategoryManager(Manager):
    def get_by_natural_key(self, category_name):
        return self.get(category_name=category_name)

class ItemManager(Manager):
    def by_date(self, date):
        return self.get_queryset().filter(
            date_added__gte=datetime.date(date,1,1),
            date_added__lte=datetime.date(date,12,31))

class ReviewManager(Manager):
    def by_date(self, date):
        return self.get_queryset().filter(
        item__date_added__gte=datetime.date(date,1,1),
        item__date_added__lte=datetime.date(date,12,31))
