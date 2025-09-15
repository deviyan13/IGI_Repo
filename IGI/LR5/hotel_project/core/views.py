import datetime
import io
from datetime import timedelta
from urllib.parse import unquote

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count
from django.shortcuts import render, get_object_or_404, redirect

from .forms import ClientForm, BookingForm, ReviewForm, PaymentForm
from .models import CompanyInfo, NewsArticle, FAQuestion, EmployeeContact, Vacancy, PromoCode, Review, Category, \
    Amenity, Room, Client, Booking, Partner, CompanyHistory, CompanyRequisite

import logging

logger = logging.getLogger(__name__)  # логгер с именем 'core.views' и пр.

# Create your views here.
import requests

def home_view(request):
    logger.debug("Запущен home_view с GET-параметрами: %s", request.GET.dict())

    FOURSQUARE_API_KEY = "fsq3qSWP4CUMB02vPmWZeJW7MMcC1jfQ4BWh/fXKIcxNzH0="

    headers = {
        "accept": "application/json",
        "Authorization": FOURSQUARE_API_KEY
    }

    params = {
        "ll": "53.911919,27.594950",
        "radius": 1000,
        "limit": 15,
        "open_now": True,
    }

    try:
        res = requests.get("https://api.foursquare.com/v3/places/search", headers=headers, params=params, timeout=5)
        res.raise_for_status()
        data = res.json()
        places = []

        for place in data.get("results", []):
            name = place.get("name")
            address = place.get("location", {}).get("formatted_address", "Без адреса")
            category = place.get("categories", [{}])[0].get("name", "Без категории")
            icon_info = place.get("categories", [{}])[0].get("icon", {})
            icon = f"{icon_info.get('prefix')}64{icon_info.get('suffix')}" if icon_info else ""
            distance = place.get("distance", "?")

            places.append({
                "name": name,
                "address": address,
                "category": category,
                "icon": icon,
                "distance": distance
            })
        logger.info("Успешно обрабатываем запрос + api")
    except Exception as e:
        logger.error(f"Foursquare API error: {e}")
        places = []


    return render(request, 'core/home.html', {
        'current_year': datetime.date.today().year,
        'news_article': NewsArticle.objects.latest('published_at'),
        'places': places,
        'partners': Partner.objects.all(),
        'featured_rooms': Room.objects.all()[:3]
    })

import calendar
from zoneinfo import ZoneInfo

def about_view(request):
    company_info = CompanyInfo.objects.order_by('-added_at').first()
    history = CompanyHistory.objects.filter(company=company_info).order_by('-year') if company_info else []
    requisites = CompanyRequisite.objects.filter(company=company_info).order_by('order') if company_info else []


    raw_tz = request.COOKIES.get('user_tz')
    if raw_tz:
        tzname = unquote(raw_tz)
        try:
            local_tz = ZoneInfo(tzname)
        except Exception:
            local_tz = ZoneInfo('UTC')
    else:
        local_tz = ZoneInfo('UTC')

    # текущее время
    now_local = datetime.datetime.now(local_tz)
    now_utc = datetime.datetime.now(ZoneInfo('UTC'))

    # формат
    def fmt(dt):
        return dt.strftime('%d/%m/%Y %H:%M:%S')

    time_local = fmt(now_local)
    time_utc = fmt(now_utc)

    # Текстовый календарь текущего месяца
    year, month = now_local.year, now_local.month
    cal = calendar.TextCalendar(firstweekday=0)
    month_calendar = cal.formatmonth(year, month).splitlines()

    return render(request, 'core/about.html', {
        'time_local': time_local,
        'time_utc': time_utc,
        'month_calendar': month_calendar,
        'current_year': datetime.date.today().year,
        'company_info': company_info,
        'history': history,
        'requisites': requisites,
        'user_tz': local_tz.key,
    })


def news_detail(request, article_id):
    article = get_object_or_404(NewsArticle, id=article_id)
    related_articles = NewsArticle.objects.exclude(id=article_id).order_by('-published_at')[:3]

    return render(request, 'core/news_detail.html', {
        'article': article,
        'related_articles': related_articles,
        'current_year': datetime.date.today().year,
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
    return render(request, 'core/privacy.html', {
        'current_year': datetime.date.today().year
    })

def jobs(request):
    vacancies = Vacancy.objects.all()
    return render(request, 'core/jobs.html', {
        'current_year': datetime.date.today().year,
        'vacancies': vacancies
    })

@login_required
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.save()
            messages.success(request, 'Отзыв успешно добавлен!')
            return redirect('core:reviews')
        else:
            messages.error(request, 'Исправьте ошибки в форме')
    else:
        form = ReviewForm()

    return render(request, 'core/add_review.html', {
        'form': form,
        'current_year': datetime.date.today().year,
    })

def reviews_list(request):
    reviews = Review.objects.select_related('author').order_by('-created_at')
    return render(request, 'core/reviews.html', {
        'reviews': reviews,
        'current_year': datetime.date.today().year,
    })

def promotions(request):
    promo_codes = PromoCode.objects.all()
    return render(request, 'core/promotions.html', {
        'current_year': datetime.date.today().year,
        'promo_codes': promo_codes,
    })


def room_catalog(request):
    categories = Category.objects.all()
    amenities = Amenity.objects.all()
    promo_codes = PromoCode.objects.filter(is_active=True)
    date_error = None

    # Инициализируем базовый QuerySet
    rooms = Room.objects.select_related('category').prefetch_related('amenities')

    # Обработка дат
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')

    if check_in and check_out:
        try:
            check_in_date = check_in
            check_out_date = check_out

            if check_out_date <= check_in_date:
                date_error = "Дата выезда должна быть после даты заезда"
                rooms = rooms.none()  # Пустой QuerySet
            else:
                # по датам только если они валидны
                rooms = rooms.exclude(
                    bookings__check_in__lte=check_out_date,
                    bookings__check_out__gte=check_in_date
                )
        except (ValueError, TypeError):
            date_error = "Некорректный формат даты"
            rooms = rooms.none()
    else:
        rooms = rooms.none()

    #  только если qs не пустой
    if rooms.exists():
        category_id = request.GET.get('category')
        amenity_ids = request.GET.getlist('amenities')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        if category_id:
            rooms = rooms.filter(category_id=category_id)

        if amenity_ids:
            rooms = rooms.filter(amenities__id__in=amenity_ids).distinct()

        if min_price:
            rooms = rooms.filter(price_per_night__gte=min_price)

        if max_price:
            rooms = rooms.filter(price_per_night__lte=max_price)


    sort = request.GET.get('sort')
    if sort == 'price_asc':
        rooms = rooms.order_by('price_per_night')
    elif sort == 'price_desc':
        rooms = rooms.order_by('-price_per_night')
    elif sort == 'popularity':
        rooms = rooms.annotate(bookings_count=Count('bookings')).order_by('-bookings_count')

    context = {
        'current_year': datetime.date.today().year,
        'categories': categories,
        'amenities': amenities,
        'promo_codes': promo_codes,
        'rooms': rooms,
        'date_error': date_error,
        'default_check_in': datetime.date.today().isoformat(),
        'default_check_out': (datetime.date.today() + timedelta(days=1)).isoformat(),
        'selected_filters': {
            'category': request.GET.get('category'),
            'amenities': request.GET.getlist('amenities'),
            'min_price': request.GET.get('min_price'),
            'max_price': request.GET.get('max_price'),
            'sort': sort,
        }
    }
    return render(request, 'core/room_catalog.html', context)

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required(login_url='account_login')
def staff_dashboard(request):
    bookings = Booking.objects.select_related('room', 'client').filter(check_out__gte=datetime.datetime.today())
    clients = Client.objects.select_related('user').all()
    return render(request, 'core/staff_dashboard.html', {
        'current_year': datetime.date.today().year,
        'bookings': bookings,
        'clients': clients,
    })

@staff_member_required(login_url='account_login')
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.delete()
        return redirect('core:staff_dashboard')
    return redirect('core:staff_dashboard')

@login_required
def delete_unpaid_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Бронь успешно удалена.')
        return redirect('core:bookings')

    return redirect('core:bookings')

@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    client, _ = Client.objects.get_or_create(user=request.user)

    # даты из GET или из POST
    if request.method == 'GET':
        check_in = request.GET.get('check_in')
        check_out = request.GET.get('check_out')
    else:
        check_in = None
        check_out = None

    client_form = ClientForm(request.POST or None, instance=client)
    booking_form = BookingForm(
        request.POST or None,
        room=room,
        initial={'check_in': check_in, 'check_out': check_out})

    if request.method == 'POST':
        if client_form.is_valid() and booking_form.is_valid():
            client_form.save()
            booking = booking_form.save(commit=False)
            booking.client = client
            booking.room = room
            days = (booking.check_out - booking.check_in).days
            booking.total_price = days * room.price_per_night
            booking.save()
            messages.success(request, 'Номер добавлен в ваши брони!')
            return redirect('core:bookings')

    return render(request, 'core/booking.html', {
        'current_year': datetime.date.today().year,
        'client_form': client_form,
        'booking_form': booking_form,
        'room': room,
    })

@login_required
def bookings_view(request):
    try:
        client = Client.objects.get(user=request.user)
        unpaid_bookings = Booking.objects.filter(client=client, status='booked')
        paid_bookings = Booking.objects.filter(client=client, status='paid')
        total_unpaid_amount = sum(booking.total_price for booking in unpaid_bookings)
        total_paid_amount = sum(booking.total_price for booking in paid_bookings)

    except Client.DoesNotExist:
        unpaid_bookings = []
        paid_bookings = []
        total_paid_amount = 0
        total_unpaid_amount = 0

    return render(request, 'core/bookings.html', {
        'unpaid_bookings': unpaid_bookings,
        'paid_bookings': paid_bookings,
        'total_paid_amount': total_paid_amount,
        'total_unpaid_amount': total_unpaid_amount,
        'current_year': datetime.date.today().year,
    })


@login_required
def payment_view(request):
    try:
        client = Client.objects.get(user=request.user)
        bookings = Booking.objects.filter(client=client, status='booked')
        total_amount = sum(booking.total_price for booking in bookings)

        if request.method == 'POST':
            for booking in bookings:
                booking.status = 'paid'
                booking.save()

            messages.success(request, 'Оплата прошла успешно!')
            return redirect('core:profile')

    except Client.DoesNotExist:
        bookings = []
        total_amount = 0

    initial_data = {
        'email': request.user.email,
        'phone': client.phone_number
    }
    form = PaymentForm(initial=initial_data)

    return render(request, 'core/payment.html', {
        'bookings': bookings,
        'total_amount': total_amount,
        'current_year': datetime.date.today().year,
        'form': form
    })

@login_required
def profile(request):
    # получаем или создаём профиль клиента
    client, created = Client.objects.get_or_create(user=request.user)
    bookings = client.bookings.filter(check_out__gte=datetime.datetime.today()).select_related('room').order_by('check_in')

    # форма для редактирования профиля
    client_form = ClientForm(request.POST or None, instance=client)
    if request.method == 'POST' and client_form.is_valid():
        client_form.save()
        return redirect('core:profile')

    cat_url = None
    try:
        cat_resp = requests.get('https://api.thecatapi.com/v1/images/search', timeout=10)
        cat_resp.raise_for_status()
        cat_data = cat_resp.json()
        if cat_data:
            cat_url = cat_data[0].get('url')
    except Exception:
        cat_url = None

    quote_text = None
    quote_author = 'Котик Пушок'
    try:
        params = {
            'method': 'getQuote',
            'format': 'json',
            'lang': 'ru'
        }
        quote_resp = requests.post(
            'http://api.forismatic.com/api/1.0/',
            data=params,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=3
        )

        quote_resp.raise_for_status()
        quote_json = quote_resp.json()
        quote_text = quote_json.get('quoteText')

        if quote_text is not None: logger.info("Успешно получили ответ  api")

        author = quote_json.get('quoteAuthor')
        if author:
            quote_text = f'“{quote_text}”'
            quote_author = f'{'Котик ' +  author}'
    except Exception:
        logger
        quote_text = None


    return render(request, 'core/profile.html', {
        'current_year': datetime.date.today().year,
        'client_form': client_form,
        'bookings': bookings,
        'cat_url': cat_url,
        'quote_text': quote_text,
        'quote_author': quote_author,
    })

@staff_member_required(login_url='account_login')
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    room = booking.room

    if request.method == 'POST':
        # привязываем форму к существующему объекту и передаём room для валидации
        form = BookingForm(request.POST or None, instance=booking, room=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Бронь успешно обновлена.')
            return redirect('core:staff_dashboard')
    else:
        form = BookingForm(instance=booking, room=room,
        initial={
            'check_in': booking.check_in.strftime('%Y-%m-%d'),
            'check_out': booking.check_out.strftime('%Y-%m-%d'),
            'guests_count': booking.guests_count,
            'include_children': booking.include_children,}
        )

    return render(request, 'core/edit_booking.html', {
        'form': form,
        'booking': booking,
        'room': room,
    })

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
from statistics import mean, median, mode

@staff_member_required(login_url='account_login')
def statistics(request):
    import os
    from django.conf import settings
    # Обеспечим папку для сохранения графиков
    stats_dir = os.path.join(settings.MEDIA_ROOT, 'media/statistics')
    os.makedirs(stats_dir, exist_ok=True)

    # 1) Клиенты в алфавитном порядке
    clients = Client.objects.order_by('last_name', 'first_name')
    client_count = clients.count()

    # 2) Общая сумма продаж и статистика по сумме каждой брони
    bookings = Booking.objects.all()
    sales = [b.total_price for b in bookings]
    total_sales = sum(sales)
    avg_sale = mean(sales) if sales else 0
    med_sale = median(sales) if sales else 0
    try:
        mode_sale = mode(sales) if sales else 0
    except:
        mode_sale = None

    # 3) Статистика по возрасту клиентов
    ages = []
    for c in clients:
        if c.birth_date:
            bd = c.birth_date
            today = datetime.date.today()
            age = (today.year - bd.year - (today.month < bd.month or today.day < bd.day))
            ages.append(age)
    avg_age = mean(ages) if ages else 0
    med_age = median(ages) if ages else 0

    # 4) Популярность категорий номеров
    category_stats = (
        Room.objects.values('category__name')
        .annotate(bookings_count=Count('bookings'))
        .order_by('-bookings_count')
    )
    popular_category = category_stats[0]['category__name'] if category_stats else None

    # 5) Прибыль по категориям
    profit_stats = (
        Booking.objects
        .values('room__category__name')
        .annotate(total_profit=Sum('total_price'))
        .order_by('-total_profit')
    )
    top_profit_category = profit_stats[0]['room__category__name'] if profit_stats else None

    # === Построение и сохранение графиков ===
    # A) Гистограмма продаж по брони
    plt.figure()
    plt.hist(sales, bins=10)
    plt.title('Распределение суммы брони')
    plt.xlabel('Сумма брони, руб')
    plt.ylabel('Число бронировавших')
    hist_path = os.path.join(stats_dir, 'hist_sales.png')
    plt.savefig(hist_path, bbox_inches='tight')
    plt.close()

    # B) Бары по популярности категории
    labels = [c['category__name'] for c in category_stats]
    counts = [c['bookings_count'] for c in category_stats]
    plt.figure()
    plt.bar(labels, counts)
    plt.title('Популярность категорий номеров')
    plt.xticks(rotation=45, ha='right')
    pop_path = os.path.join(stats_dir, 'bar_popularity.png')
    plt.savefig(pop_path, bbox_inches='tight')
    plt.close()

    # C) Линейный график прибыли по категориям
    labels2 = [p['room__category__name'] for p in profit_stats]
    profits = [p['total_profit'] for p in profit_stats]
    plt.figure()
    plt.plot(labels2, profits, marker='o')
    plt.title('Прибыль по категориям номеров')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Прибыль, руб')
    profit_path = os.path.join(stats_dir, 'line_profit.png')
    plt.savefig(profit_path, bbox_inches='tight')
    plt.close()

    # Ссылки для шаблона
    hist_url = settings.MEDIA_URL + 'media/statistics/hist_sales.png'
    pop_url = settings.MEDIA_URL + 'media/statistics/bar_popularity.png'
    profit_url = settings.MEDIA_URL + 'media/statistics/line_profit.png'

    return render(request, 'core/statistics.html', {
        'clients': clients,
        'client_count': client_count,
        'total_sales': total_sales,
        'avg_sale': avg_sale,
        'med_sale': med_sale,
        'mode_sale': mode_sale,
        'avg_age': avg_age,
        'med_age': med_age,
        'popular_category': popular_category,
        'top_profit_category': top_profit_category,
        'hist_url': hist_url,
        'pop_url': pop_url,
        'profit_url': profit_url,
    })



