from django.contrib import admin

from .models import CompanyInfo, NewsArticle, FAQuestion, EmployeeContact, Vacancy, Review, PromoCode


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