# core/forms.py
from allauth.account.forms import SignupForm
from django import forms
from django.core.exceptions import ValidationError

from .models import Client, Booking

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'middle_name', 'phone_number', 'age']
        widgets = {
            'first_name': forms.TextInput(attrs={'required': True}),
            'last_name': forms.TextInput(attrs={'required': True}),
            'middle_name': forms.TextInput(),
            'phone_number': forms.TextInput(attrs={
                'required': True,
                'placeholder': '+375 (12) 345-67-89',
                'pattern': r'\+375\s*\(\d{2}\)\s*\d{3}-\d{2}-\d{2}',
                'title': '+375 (XX) XXX-XX-XX',
            }),
            'age': forms.NumberInput(attrs={
                'required': True,
                'type': 'number',
                'min': '18',
                'max': '120',
                'step': '1',
                'title': 'Только целые числа от 1 до 120',
            }),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'middle_name': 'Отчество',
            'age': 'Возраст',
            'phone_number': 'Номер телефона'
        }

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label="Имя", required=True)
    last_name = forms.CharField(max_length=30, label="Фамилия", required=True)
    middle_name = forms.CharField(max_length=30, label="Отчество", required=False)
    age = forms.NumberInput()

    class Meta(ClientForm.Meta):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in ClientForm().fields.items():
            self.fields[name] = field

        pwd1 = self.fields.get('password1')
        if pwd1:
            pwd1.widget.attrs.update({
                'required': 'required',
                'minlength': '8',
                'oninvalid': "this.setCustomValidity('Пароль должен содержать минимум 8 символов и не быть слишком простым')",
                'oninput': "this.setCustomValidity('')"
            })
        pwd2 = self.fields.get('password2')
        if pwd2:
            pwd2.widget.attrs.update({
                'required': 'required',
                'oninvalid': "this.setCustomValidity('Пожалуйста, введите пароль ещё раз для подтверждения')",
                'oninput': "this.setCustomValidity('')"
            })

    def save(self, request):
        user = super().save(request)
        Client.objects.get_or_create(
            user=user,
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            middle_name=self.cleaned_data['middle_name'],
            phone_number=self.cleaned_data['phone_number'],
            age=self.cleaned_data['age'],
        )
        return user



class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in', 'check_out', 'guests_count', 'include_children']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
            'guests_count': forms.NumberInput(
                attrs={
                    'type': 'number',
                    'min': '1',
                }
            )
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

        if self.room:
            self.fields['guests_count'].widget.attrs['max'] = self.room.capacity
            self.fields['guests_count'].help_text = f"Максимальное количество гостей: {self.room.capacity}"

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