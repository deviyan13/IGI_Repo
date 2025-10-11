from django.utils import timezone
import pytz

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            tz = request.user.timezone  # предполагаем, что у пользователя есть поле timezone
            timezone.activate(pytz.timezone(tz))
        else:
            timezone.deactivate()
        return self.get_response(request)