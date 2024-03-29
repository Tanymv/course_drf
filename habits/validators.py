from datetime import timedelta

from rest_framework.serializers import ValidationError

from habits.models import Habit


class RelatedOrRewardValidator:
    """Проверка заполнения полей связанной привычки и вознаграждения:
     может быть заполнено только одно поле"""

    def __call__(self, value):
        if value.get('related_habit') and value.get('reward'):
            raise ValidationError('Поле связанной привычки и поле вознаграждения не могут быть заполнены '
                                  'одновременно, выберите одно из двух полей')


class NiceHabitValidator:
    """Проверка на отсутствие у приятной привычки полей
    связанной привычки и вознаграждения"""

    def __call__(self, value):
        if value.get('is_nice'):
            if value.get('related_habit') or value.get('reward'):
                raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки.')


class RelatedHabitValidator:
    """Проверка на принадлежность связанной привычки к приятным:
    Связать с полезной привычкой можно только приятную
    """

    def __call__(self, value):
        related_habit = value.get('related_habit')
        if related_habit:
            obj = Habit.objects.get(id=related_habit.id)
            if not obj.is_nice:
                raise ValidationError(
                    'В связанные привычки могут попадать только привычки с признаком приятной привычки.')


def duration_validator(duration):
    """Проверка продолжительности выполнения привычки:
     Должна быть не более 2 минут"""

    if duration > timedelta(minutes=2):
        raise ValidationError('Время выполнения должно быть не больше 120 секунд.')