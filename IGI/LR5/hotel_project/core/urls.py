from django.urls import path, re_path
from . import views

app_name = 'core'
urlpatterns = [
    path('',            views.home_view,    name='home'),
    path('about/',      views.about_view,   name='about'),
    path('news/',       views.news_list,    name='news'),
    path('glossary/',   views.faq,          name='faq'),
    path('contacts/',   views.contacts,     name='contacts'),
    path('privacy/',    views.privacy,      name='privacy'),
    path('jobs/',       views.jobs,         name='jobs'),
    path('reviews/',    views.reviews_list, name='reviews'),
    path('reviews/add/',views.add_review,   name='add_review'),
    path('promo/',      views.promotions,   name='promotions'),

]