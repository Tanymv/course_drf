from celery import shared_task
from django.utils import timezone
from habits.models import Habit
from services import MyBot, change_start_date


@shared_task
def send_tg_reminder_task():
    """Ежедневное задание:
    Отправить напоминание о выполнение привычки, если дата авполнения == сегодняшней
    """
    habits = Habit.objects.filter(start_date=timezone.now().date())
    my_bot = MyBot()
    for h in habits:
        text = f'Напоминаю! Сегодня {h}'
        chat_id = h.user.telegram_id
        my_bot.send_message(chat_id, text)
        change_start_date(h)