from django.utils import timezone
import pytz


def get_timezones(request):
    return {
        'timezones': pytz.common_timezones,
        'current_time': timezone.localtime(timezone.now())
    }
