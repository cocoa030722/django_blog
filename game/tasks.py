from celery import shared_task
from pytz import timezone
import datetime
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import MainUser

channel_layer = get_channel_layer()

@shared_task
def my_scheduled_task():
    cutoff_time = datetime.datetime.now(timezone('Asia/Seoul')) - datetime.timedelta(minutes=1)
    old_games = MainUser.objects.filter(created_at__lt=cutoff_time)
    old_games.delete()
    print('Task completed!')