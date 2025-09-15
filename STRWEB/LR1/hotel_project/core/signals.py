from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from .models import Client

@receiver(user_signed_up)
def create_client_profile(request, user, **kwargs):
    """
    При первой регистрации (в том числе через Google) создаём профиль Client
    и заполняем ФИО из данных соц. аккаунта, если они есть.
    """
    # Проверяем, есть ли у пользователя socialaccount
    social_accounts = user.socialaccount_set.all()
    if social_accounts:
        extra = social_accounts[0].extra_data

        first = extra.get('given_name') or ''
        last = extra.get('family_name') or ''

        Client.objects.get_or_create(
            user=user,
            defaults={
                'first_name': first,
                'last_name': last,
                'middle_name': '',
                'phone_number': '',
            }
        )


