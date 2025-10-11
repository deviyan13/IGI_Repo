from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from ..models import Category, Room, Client, Booking

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
            user=None,
            first_name='Иван',
            last_name='Иванов',
            birth_date=date(1990,1,1),
            phone_number='+375 (29) 123-45-67'
        )

    def test_room_str(self):
        self.assertEqual(str(self.room), 'Номер 101')  # __str__ модели Room

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
