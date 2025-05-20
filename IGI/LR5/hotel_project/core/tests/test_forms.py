from django.test import TestCase
from datetime import date, timedelta
from ..forms import ClientForm, BookingForm
from ..models import Room, Client

class FormsTestCase(TestCase):
    def setUp(self):
        self.room = Room.objects.create(number=1, category_id=1, capacity=3, price_per_night=1000)
        self.client0 = Client.objects.create(
            user=None, first_name='A', last_name='B',
            birth_date=date(2010,1,1), phone_number='+375 (29) 111-11-11'
        )

    def test_client_form_valid_data(self):
        # Исправим birth_date на ≥18 лет
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
        self.assertIn('__all__', form.errors)  # общая ошибка дат
