# core/forms.py
from django import forms
from django.core.exceptions import ValidationError

from .models import Client, Booking

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'middle_name', 'ages']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'middle_name': 'Отчество',
            'ages': 'Возраст',
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in', 'check_out', 'guests_count', 'include_children']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'check_in': 'Дата заезда',
            'check_out': 'Дата выезда',
            'guests_count': 'Кол-во гостей',
            'include_children': 'С детьми',
        }

    def __init__(self, *args, room=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.room = room

    def clean_guests_count(self):
        guests = self.cleaned_data.get('guests_count')
        if self.room and guests > self.room.capacity:
            raise ValidationError(f"Максимальное количество гостей для этого номера: {self.room.capacity}.")
        return guests

    def clean(self):
        cleaned = super().clean()
        check_in = cleaned.get('check_in')
        check_out = cleaned.get('check_out')
        if check_in and check_out and check_in >= check_out:
            raise ValidationError('Дата выезда должна быть позже даты заезда.')
        for booking in Booking.objects.all():
            if booking.room == self.room and (booking.check_in < check_out and booking.check_out > check_in):
                print(booking.check_in, booking.check_out)
                raise ValidationError('В выбранном вами промежутке дат этот номер занят.')

        return cleaned