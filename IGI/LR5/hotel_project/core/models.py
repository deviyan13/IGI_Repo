from django.core.validators import MinValueValidator, RegexValidator, MaxValueValidator
from django.db import models
from django.conf import settings


# Create your models here.

class CompanyInfo(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Описание гостиницы')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')

    def __str__(self):
        return f'{self.title} ({self.added_at})'


class NewsArticle(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(max_length=250, verbose_name='Новость')
    image = models.ImageField(upload_to='media/news/', blank=True, default='media/news/default_news.png', verbose_name='Картинка')
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.title


class FAQuestion(models.Model):
    question = models.CharField(max_length=150, verbose_name='Вопрос')
    answer = models.CharField(max_length=150, verbose_name='Ответ')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')

    def __str__(self):
        return self.question


class EmployeeContact(models.Model):
    name = models.CharField(max_length=100, verbose_name='ФИО сотрудника')
    position = models.CharField(max_length=100, verbose_name='Должность')
    photo = models.ImageField(upload_to='media/contacts/', verbose_name='Фото сотрудника',
                              default='media/contacts/default.png', blank=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Электронная почта')


class Vacancy(models.Model):
    title = models.CharField(max_length=200, verbose_name='Должность')
    description = models.TextField(verbose_name='Описание вакансии')
    posted_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата размещения')

    def __str__(self):
        return self.title


class Review(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    rating = models.PositiveSmallIntegerField(
        verbose_name='Оценка (1–5)',
        choices=[(i, i) for i in range(1, 6)]
    )
    text = models.TextField(verbose_name='Текст отзыва')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')

    def __str__(self):
        return f'{self.author.username} — {self.rating}'


class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='Код')
    discount_percent = models.PositiveSmallIntegerField(verbose_name='Скидка (%)')
    valid_from = models.DateField(verbose_name='Начало действия')
    valid_to = models.DateField(verbose_name='Окончание действия')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    def __str__(self):
        return self.code


class Category(models.Model):
    CLASS_CHOICES = [
        ('lux', 'Люкс'),
        ('semi_lux', 'Полулюкс'),
        ('standard', 'Обычный'),
    ]
    name = models.CharField(
        max_length=20,
        choices=CLASS_CHOICES,
        unique=True,
        verbose_name='Класс номера'
    )
    description = models.TextField(verbose_name='Описание категории')

    def __str__(self):
        return dict(self.CLASS_CHOICES).get(self.name, self.name)


class Amenity(models.Model):
    name = models.CharField(max_length=50, verbose_name='Удобство')

    def __str__(self):
        return self.name


class Room(models.Model):
    number = models.CharField(max_length=10, unique=True, verbose_name='Номер')
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='rooms',
        verbose_name='Категория'
    )
    capacity = models.PositiveIntegerField(verbose_name='Вместимость')
    price_per_night = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Цена за ночь'
    )
    amenities = models.ManyToManyField(
        Amenity,
        blank=True,
        related_name='rooms',
        verbose_name='Удобства'
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    photo = models.ImageField(
        upload_to='media/rooms/',
        blank=True,
        null=True,
        default='media/rooms/default.jpeg',
        verbose_name='Фото номера',
    )

    def __str__(self):
        return f"Номер {self.number} ({self.category})"


class Client(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_profile',
        verbose_name='Пользователь'
    )
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=30, blank=True, verbose_name='Отчество')
    age = models.SmallIntegerField(verbose_name='Возраст', validators=[
        MinValueValidator(18),
        MaxValueValidator(120),
    ])
    phone_number = models.CharField(max_length=19, verbose_name='Номер телефона', validators=[
        RegexValidator(
            regex=r'\s*\+375\s*\(\d{2}\)\s*\d{3}-\d{2}-\d{2}\s*$',
            message='формат белорусского номера: +375 (XX) XXX-XX-XX')
    ])

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}".strip()


class Booking(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='Клиент'
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        related_name='bookings',
        verbose_name='Номер'
    )
    check_in = models.DateField(verbose_name='Дата заезда')
    check_out = models.DateField(verbose_name='Дата выезда')
    guests_count = models.IntegerField(verbose_name='Кол-во гостей')
    include_children = models.BooleanField(default=False, verbose_name='С детьми')
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Итоговая цена'
    )

    def __str__(self):
        return f"Бронь {self.id}: {self.client} — {self.room}"


class Payment(models.Model):
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='payment',
        verbose_name='Бронирование'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма'
    )
    paid_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')

    def __str__(self):
        return f"Платёж за бронь {self.booking.id}: {self.amount}"
