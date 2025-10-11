from django.test import TestCase, Client as DjangoClient
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Room, Category, Client as ClientProfile

class ViewsTestCase(TestCase):
    def setUp(self):
        # создаём тестового пользователя и логинимся
        self.user = User.objects.create_user('user1','u@e.com','pass')
        self.client = DjangoClient()
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
