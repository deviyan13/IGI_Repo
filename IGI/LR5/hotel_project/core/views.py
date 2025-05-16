import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import CompanyInfo, NewsArticle, FAQuestion, EmployeeContact, Vacancy, PromoCode, Review


# Create your views here.

def home_view(request):
    return render(request, 'core/home.html', {'current_year': datetime.date.today().year})

def about_view(request):
    company_info = CompanyInfo.objects.order_by('-added_at').first()

    return render(request, 'core/about.html', {
        'current_year': datetime.date.today().year,
        'company_info': company_info,
    })

def news_list(request):
    news_article = NewsArticle.objects.order_by('-published_at')

    return render(request, 'core/news.html', {
        'current_year': datetime.date.today().year,
        'news_articles': news_article,
    })

def faq(request):
    faqs = FAQuestion.objects.order_by('-added_at')

    return render(request, 'core/faq.html', {
        'current_year': datetime.date.today().year,
        'faqs': faqs,
    })

def contacts(request):
    contacts_list = EmployeeContact.objects.order_by('name')

    return render(request, 'core/contacts.html', {
        'current_year': datetime.date.today().year,
        'contacts': contacts_list,
    })

def privacy(request):
    return render(request, 'core/privacy.html', {'current_year': datetime.date.today().year})

def jobs(request):
    vacancies = Vacancy.objects.all()
    return render(request, 'core/jobs.html', {
        'current_year': datetime.date.today().year,
        'vacancies': vacancies
    })

@login_required
def add_review(request):
    # здесь логика формы для добавления отзыва
    ...

def reviews_list(request):
    reviews = Review.objects.select_related('author').all()
    return render(request, 'core/reviews.html', {
        'reviews': reviews,
    })

def promotions(request):
    promo_codes = PromoCode.objects.all()
    return render(request, 'core/promotions.html', {
        'current_year': datetime.date.today().year,
        'promo_codes': promo_codes,
    })



