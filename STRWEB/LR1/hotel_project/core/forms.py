import datetime
import re

from allauth.account.forms import SignupForm
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator

from .models import Client, Booking

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'middle_name', 'phone_number', 'birth_date']
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
            'birth_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'required': True,
                    # указываем max = сегодня-18 лет
                    'max': (datetime.date.today().replace(year=datetime.date.today().year - 18)).isoformat(),
                    'title': 'Вам должно быть не менее 18 лет',
                }
            ),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'middle_name': 'Отчество',
            'birth_date': 'Дата рождения',
            'phone_number': 'Номер телефона'
        }

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label="Имя", required=True)
    last_name = forms.CharField(max_length=30, label="Фамилия", required=True)
    middle_name = forms.CharField(max_length=30, label="Отчество", required=False)
    birth_date = forms.DateField(label='Дата рождения', validators=[
        MaxValueValidator(datetime.date.today().replace(year=datetime.date.today().year - 18)),
    ])

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
            birth_date=self.cleaned_data['birth_date'],
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

        qs = Booking.objects.filter(
            room=self.room,
            check_in__lte=check_out,
            check_out__gte=check_in
        )
        #  существующую бронь исключаем из queryset
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError('В выбранном вами промежутке дат этот номер занят.')

        # for booking in Booking.objects.all():
        #     if booking.room == self.room and (booking.check_in < check_out and booking.check_out > check_in):
        #         raise ValidationError('В выбранном вами промежутке дат этот номер занят.')

        return cleaned

from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Напишите ваш отзыв...'
            }),
            'rating': forms.Select(choices=[(i, f'{i} звезд') for i in range(1, 6)])
        }
        labels = {
            'text': 'Текст отзыва',
            'rating': 'Ваша оценка'
        }

class PaymentForm(forms.Form):
    card_number = forms.CharField(
        max_length=19,
        min_length=13,
        label="Номер карты",
        widget=forms.TextInput(attrs={
            'required': True,
            'placeholder': '1234 5678 9012 3456',
            'pattern': '[0-9\\s]{13,19}',
            'title': 'Введите номер карты (13-19 цифр)',
        }),
        error_messages={
            'required': 'Поле "Номер карты" обязательно для заполнения',
            'min_length': 'Номер карты должен содержать не менее 13 цифр',
            'max_length': 'Номер карты должен содержать не более 19 цифр'
        }
    )

    expiry_date = forms.CharField(
        max_length=5,
        label="Срок действия",
        widget=forms.TextInput(attrs={
            'required': True,
            'placeholder': 'ММ/ГГ',
            'pattern': '(0[1-9])|(1[0-2])\/[0-9]{2}',
            'title': 'Формат: ММ/ГГ (например, 12/24)',
        }),
        error_messages={'required': 'Поле "Срок действия" обязательно для заполнения'}
    )

    cvv = forms.CharField(
        max_length=3,
        min_length=3,
        label="CVV",
        widget=forms.TextInput(attrs={
            'required': True,
            'placeholder': '123',
            'pattern': '[0-9]{3}',
            'title': '3 цифры с обратной стороны карты',
        }),
        error_messages={
            'required': 'Поле "CVV" обязательно для заполнения',
            'min_length': 'CVV должен содержать 3 цифры',
            'max_length': 'CVV должен содержать 3 цифры'
        }
    )

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'required': True,
            'placeholder': 'ваш@email.com',
        }),
        error_messages={
            'required': 'Поле "Email" обязательно для заполнения',
            'invalid': 'Введите корректный email адрес'
        }
    )

    phone = forms.CharField(
        max_length=19,
        label="Телефон",
        widget=forms.TextInput(attrs={
            'required': True,
            'placeholder': '+375 (29) 123-45-67',
            'pattern': '\\s*\\+375\\s*\\(\\d{2}\\)\\s*\\d{3}-\\d{2}-\\d{2}\\s*$',
            'title': 'Формат: +375 (XX) XXX-XX-XX',
        }),
        error_messages={'required': 'Поле "Телефон" обязательно для заполнения'}
    )

    def clean_card_number(self):
        card_number = self.cleaned_data['card_number']
        card_number = re.sub(r'\D', '', card_number)

        if not card_number.isdigit():
            raise forms.ValidationError('Номер карты должен содержать только цифры')

        def luhn_check(card_number):
            def digits_of(n):
                return [int(d) for d in str(n)]

            digits = digits_of(card_number)
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            checksum = sum(odd_digits)
            for d in even_digits:
                checksum += sum(digits_of(d * 2))
            return checksum % 10 == 0

        if not luhn_check(card_number):
            raise forms.ValidationError('Неверный номер карты')

        return card_number

    def clean_expiry_date(self):
        expiry_date = self.cleaned_data['expiry_date']

        if not re.match(r'^\d{2}/\d{2}$', expiry_date):
            raise forms.ValidationError('Используйте формат ММ/ГГ (например, 12/24)')

        month, year = expiry_date.split('/')

        if not (1 <= int(month) <= 12):
            raise forms.ValidationError('Месяц должен быть от 01 до 12')

        current_year = datetime.now().year % 100
        current_month = datetime.now().month

        if int(year) < current_year or (int(year) == current_year and int(month) < current_month):
            raise forms.ValidationError('Срок действия карты истек')

        return expiry_date

    def clean_cvv(self):
        cvv = self.cleaned_data['cvv']

        if not cvv.isdigit():
            raise forms.ValidationError('CVV должен содержать только цифры')

        return cvv

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        phone = re.sub(r'[^\d+]', '', phone)

        if not re.match(r'\+375\s*\(\d{2}\)\s*\d{3}-\d{2}-\d{2}', phone):
            raise forms.ValidationError('Введите номер в формате +375 (XX) XXX-XX-XX')

        return phone