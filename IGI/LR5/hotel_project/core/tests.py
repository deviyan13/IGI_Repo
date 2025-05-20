from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from datetime import date, timedelta
from .forms import ClientForm, BookingForm
from .models import Room, Client, Category, Booking


class FormsTestCase(TestCase):
    def setUp(self):
        # 1) Создаём категорию для комнаты
        category = Category.objects.create(name='Тестовая категория')
        # 2) Создаём комнату с обязательным свойством category
        self.room = Room.objects.create(
            number=1,
            category=category,
            capacity=3,
            price_per_night=1000
        )
        # 3) Клиент для тестов валидации формы
        self.client0 = Client.objects.create(
            user=User.objects.create_user('TestUser'),
            first_name='A',
            last_name='B',
            birth_date=date(2000,1,1),
            phone_number='+375 (29) 111-11-11'
        )

    def test_client_form_valid_data(self):
        # Исправим birth_date на >= 18 лет
        data = {
            'first_name':'Иван','last_name':'Иванов','middle_name':'Иваныч',
            'phone_number':'+375 (29) 123-45-67','birth_date':'1990-01-01'
        }
        form = ClientForm(data=data, instance=self.client0)
        self.assertTrue(form.is_valid())

    def test_client_form_underage(self):
        # Пользователю 10 лет — должно быть ошибкой
        data = {
            'first_name':'Мал','last_name':'Ой','phone_number':'+375 (29) 123-45-67',
            'birth_date': date.today().strftime('%Y-%m-%d')
        }
        form = ClientForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('birth_date', form.errors)

    def test_booking_form_date_validation(self):
        # check_out ≤ check_in
        data = {
            'check_in': date.today(),
            'check_out': date.today(),
            'guests_count':1,
            'include_children':False
        }
        form = BookingForm(data=data, room=self.room)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

from django.core.exceptions import ValidationError
from datetime import date, timedelta


class ModelsTestCase(TestCase):
    def setUp(self):

        self.category = Category.objects.create(name='Обычный')

        self.room = Room.objects.create(
            number=101,
            category=self.category,
            capacity=2,
            price_per_night=1500
        )

        self.client0 = Client.objects.create(
            user=User.objects.create_user('TestUser'),
            first_name='Иван',
            last_name='Иванов',
            birth_date=date(1990,1,1),
            phone_number='+375 (29) 123-45-67'
        )

    def test_room_str(self):
        self.assertEqual(str(self.room), 'Номер 101 (Обычный)')  # __str__ модели Room

    def test_booking_creation_and_price(self):
        check_in  = date.today()
        check_out = check_in + timedelta(days=3)
        booking = Booking.objects.create(
            client=self.client0,
            room=self.room,
            check_in=check_in,
            check_out=check_out,
            guests_count=2,
            include_children=False,
            total_price=3 * self.room.price_per_night
        )
        self.assertEqual(booking.total_price, 4500)
        self.assertTrue(booking.pk)

    def test_booking_capacity_validation(self):
        # попытка забронировать больше гостей, чем вместимость
        b = Booking(
            client=self.client0,
            room=self.room,
            check_in=date.today(),
            check_out=date.today() + timedelta(days=1),
            guests_count=5,
            include_children=False,
            total_price=1500
        )
        with self.assertRaises(ValidationError):
            b.full_clean()  # вызываем валидацию моделей :contentReference[oaicite:2]{index=2}

from django.urls import reverse
from django.contrib.auth.models import User
from .models import Room, Category, Client as ClientProfile


class ViewsTestCase(TestCase):
    def setUp(self):
        # создаём тестового пользователя и логинимся
        self.user = User.objects.create_user('user1','u@e.com','pass')
        self.client.login(username='user1', password='pass')

        # создаём необходимые объекты
        cat = Category.objects.create(name='Стандарт')
        self.room = Room.objects.create(number=10, category=cat, capacity=2, price_per_night=1200)

    def test_room_catalog_view(self):
        url = reverse('core:room_catalog')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'core/room_catalog.html')
        self.assertIn('rooms', resp.context)
        # комната должна оказаться в контексте
        self.assertIn(self.room, resp.context['rooms'])

    def test_book_room_redirect_if_not_logged(self):
        # логаутимся и пробуем забронировать
        self.client.logout()
        url = reverse('core:book_room', args=[self.room.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)  # редирект на логин

    def test_book_room_success(self):
        url = reverse('core:book_room', args=[self.room.id])
        data = {
            'first_name':'Иван','last_name':'Иванов','middle_name':'','phone_number':'+375 (29) 123-45-67',
            'birth_date':'1990-01-01',
            'check_in':'2025-06-01','check_out':'2025-06-03','guests_count':1,'include_children':False
        }
        resp = self.client.post(url, data)
        # после успешного бронирования — редирект в профиль
        self.assertRedirects(resp, reverse('core:profile'))
        # профиль пользователя должен содержать бронь
        profile = ClientProfile.objects.get(user=self.user)
        self.assertTrue(profile.bookings.exists())
