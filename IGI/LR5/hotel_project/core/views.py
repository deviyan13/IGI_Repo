import datetime
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect

from .forms import ClientForm, BookingForm, ReviewForm
from .models import CompanyInfo, NewsArticle, FAQuestion, EmployeeContact, Vacancy, PromoCode, Review, Category, \
    Amenity, Room, Client, Booking


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
@login_required
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user  # Используем правильное имя поля
            review.save()
            messages.success(request, 'Отзыв успешно добавлен!')
            return redirect('core:reviews')
        else:
            messages.error(request, 'Исправьте ошибки в форме')
    else:
        form = ReviewForm()

    return render(request, 'core/add_review.html', {'form': form})

def reviews_list(request):
    reviews = Review.objects.select_related('author').order_by('-created_at')
    return render(request, 'core/reviews.html', {
        'reviews': reviews,
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
                    bookings__check_in__lt=check_out_date,
                    bookings__check_out__gt=check_in_date
                )
        except (ValueError, TypeError):
            date_error = "Некорректный формат даты"
            rooms = rooms.none()
    else:
        rooms = rooms.none()

    # Фильтрация только если QuerySet не пустой
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

    context = {
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
        }
    }
    return render(request, 'core/room_catalog.html', context)

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required(login_url='account_login')
def staff_dashboard(request):
    bookings = Booking.objects.select_related('room', 'client').filter(check_out__gte=datetime.datetime.today())
    clients = Client.objects.select_related('user').all()
    return render(request, 'core/staff_dashboard.html', {
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
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    client, _ = Client.objects.get_or_create(user=request.user)

    # даты из GET или из POST (при сабмите)
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
            return redirect('core:profile')

    return render(request, 'core/booking.html', {
        'client_form': client_form,
        'booking_form': booking_form,
        'room': room,
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

    return render(request, 'core/profile.html', {
        'client_form': client_form,
        'bookings': bookings,
    })
