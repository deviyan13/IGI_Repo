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
    path('rooms/',      views.room_catalog, name='room_catalog'),
    path('rooms/<int:room_id>/book/', views.book_room, name='book_room'),
    # Панель сотрудника
    path('staff/',      views.staff_dashboard, name='staff_dashboard'),
    path('profile/',    views.profile,      name='profile')
]