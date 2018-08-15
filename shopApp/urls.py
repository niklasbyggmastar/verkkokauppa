from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('?<int:item_id>/', views.info, name='info'),
    path('results/<category_name>/', views.results, name='results'),
    path('buy/<int:item_id>/', views.buy, name='buy'),
    path('write/<int:item_id>/', views.write, name='write'),
    path('login_view/', views.login_view, name='login_view'),
    path('signup/', views.signup, name='signup'),
    path('account/', views.account, name='account'),
    #---- Actions ----
    path('add/', views.add, name='add'),
    path('post_review/<int:item_id>/', views.post_review, name='post_review'),
    path('login_action/', views.login_action, name='login_action'),
    path('logout_action/', views.logout_action, name='logout_action'),
    path('check_email/', views.check_email, name='check_email'),

]
