import datetime

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect

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

# Helper to check staff group
def is_staff_user(user):
    return user.is_authenticated and user.groups.filter(name='Staff').exists()

def room_catalog(request):
    categories = Category.objects.all()
    amenities = Amenity.objects.all()
    promo_codes = PromoCode.objects.filter(is_active=True)

    # Base queryset
    rooms = Room.objects.select_related('category').prefetch_related('amenities').all()
    # Filtering
    category_id = request.GET.get('category')
    amenity_id = request.GET.get('amenity')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if category_id:
        rooms = rooms.filter(category_id=category_id)
    if amenity_id:
        rooms = rooms.filter(amenities__id=amenity_id)
    if min_price:
        rooms = rooms.filter(price_per_night__gte=min_price)
    if max_price:
        rooms = rooms.filter(price_per_night__lte=max_price)

    context = {
        'categories': categories,
        'amenities': amenities,
        'promo_codes': promo_codes,
        'rooms': rooms,
    }
    return render(request, 'core/room_catalog.html', context)

@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    client = get_object_or_404(Client, user=request.user)
    available_rooms = []
    error = None

    if request.method == 'POST':
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        guests_count = int(request.POST.get('guests_count', 1))
        include_children = 'include_children' in request.POST

        # validate date logic
        if check_in >= check_out:
            error = 'Дата выезда должна быть позже даты заезда.'
        elif guests_count > room.capacity:
            error = 'Превышена вместимость номера.'
        else:
            # Here you would check for overlapping bookings in real logic
            total_days = (
                    datetime.timezone.datetime.fromisoformat(check_out) - datetime.timezone.datetime.fromisoformat(check_in)).days
            total_price = total_days * room.price_per_night
            booking = Booking.objects.create(
                client=client,
                room=room,
                check_in=check_in,
                check_out=check_out,
                guests_count=guests_count,
                include_children=include_children,
                total_price=total_price
            )
            return redirect('core:staff_dashboard')

    # On GET or error, list this room only
    available_rooms = [room]
    context = {
        'available_rooms': available_rooms,
        'error': error,
    }
    return render(request, 'core/booking.html', context)

@user_passes_test(is_staff_user)
def staff_dashboard(request):
    bookings = Booking.objects.select_related('room', 'client').filter(check_out__gte=datetime.timezone.now().date())
    clients = Client.objects.select_related('user').all()
    return render(request, 'core/staff_dashboard.html', {
        'bookings': bookings,
        'clients': clients,
    })

