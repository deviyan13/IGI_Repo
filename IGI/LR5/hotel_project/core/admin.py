from django.contrib import admin

from .models import *


# Register your models here.

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'content')

@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'image')

@admin.register(FAQuestion)
class FAQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')

@admin.register(EmployeeContact)
class FAQuestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'photo', 'phone', 'email')

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'posted_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'rating', 'text', 'created_at')

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'valid_from', 'valid_to', 'is_active')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Amenity)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'category', 'price_per_night', 'description', 'photo')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'age', 'middle_name', )

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client', 'room', 'check_in', 'check_out', 'guests_count', 'include_children', 'total_price')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'paid_at')