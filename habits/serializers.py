from rest_framework import serializers
from habits.models import Habit
from habits.validators import RelatedOrRewardValidator, NiceHabitValidator, RelatedHabitValidator, duration_validator


class HabitSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для модели привычки"""
    duration = serializers.DurationField(validators=[duration_validator])

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            RelatedOrRewardValidator(),
            NiceHabitValidator(),
            RelatedHabitValidator()
        ]