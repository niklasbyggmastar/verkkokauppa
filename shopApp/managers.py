from django.db.models.manager import Manager
import datetime

class CategoryManager(Manager):
    def by_name(self, name):
        return self.get_queryset().filter(name=name)

class ProfileManager(Manager):
    def by_user(self, user):
        return self.get_queryset().filter(id=user.id)

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

class OrderManager(Manager):
    def by_user(self, user):
        return self.get_queryset().filter(id=user.id) #API loppuun
