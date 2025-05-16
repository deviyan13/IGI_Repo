from django.db import models

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
    image = models.ImageField(upload_to='static/news/', blank=True, default='static/news/default_news.png', verbose_name='Картинка')
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
    photo = models.ImageField(upload_to='static/contacts/', verbose_name='Фото сотрудника',
                              default='static/contacts/default.png', blank=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Электронная почта')

class Vacancy(models.Model):
    title = models.CharField(max_length=200, verbose_name='Должность')
    description = models.TextField(verbose_name='Описание вакансии')
    posted_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата размещения')

    def __str__(self):
        return self.title

from django.conf import settings

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
