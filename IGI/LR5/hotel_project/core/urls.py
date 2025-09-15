from django.urls import path, re_path
from . import views

app_name = 'core'
urlpatterns = [
    re_path(r'^$', views.home_view, name='home'),
    re_path(r'^about/$', views.about_view, name='about'),
    re_path(r'^news/$', views.news_list, name='news'),
    re_path(r'^glossary/$', views.faq, name='faq'),
    re_path(r'^contacts/$', views.contacts, name='contacts'),
    re_path(r'^privacy/$', views.privacy, name='privacy'),
    re_path(r'^jobs/$', views.jobs, name='jobs'),
    re_path(r'^reviews/$', views.reviews_list, name='reviews'),
    re_path(r'^reviews/add/$', views.add_review, name='add_review'),
    re_path(r'^promo/$', views.promotions, name='promotions'),
    re_path(r'^rooms/$', views.room_catalog, name='room_catalog'),
    re_path(r'^rooms/(?P<room_id>\d+)/book/$', views.book_room, name='book_room'),
    re_path(r'^profile/$', views.profile, name='profile'),
    # панель сотрудника
    re_path(r'^staff/$', views.staff_dashboard, name='staff_dashboard'),
    re_path(r'^delete-booking/(?P<booking_id>\d+)/$', views.delete_booking, name='delete_booking'),
    re_path(r'^staff/bookings/(?P<booking_id>\d+)/edit/$', views.edit_booking, name='edit_booking'),
    re_path(r'^staff/statistics/$',views.statistics, name='statistics'),
    #брони
    re_path(r'^bookings/$', views.bookings_view, name='bookings'),
    re_path(r'^bookings/delete/(?P<booking_id>\d+)/$', views.delete_unpaid_booking, name='delete_unpaid_booking'),
    # re_path(r'^bookings/update/(?P<booking_id>\d+)/$', views.update_booking_cart, name='update_booking'),
    re_path(r'^payment/$', views.payment_view, name='payment'),
    re_path(r'^news/(?P<article_id>\d+)/$', views.news_detail, name='news_detail'),

]