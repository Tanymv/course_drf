from rest_framework import generics

from habits.models import Habit
from habits.serializers import HabitSerializer
from users.permissions import IsOwner


class HabitListView(generics.ListAPIView):
    """Контроллер просмотра списка опубликованых привычек"""
    serializer_class = HabitSerializer

    def get_queryset(self):
        """Фильтруем подборку по признаку публикации"""
        return Habit.objects.filter(is_published=True)


class UserHabitListView(generics.ListAPIView):
    """Контроллер просмотра списка привычек текущего пользователя"""
    serializer_class = HabitSerializer

    def get_queryset(self):
        """Фильтруем подборку по текущему пользователю"""
        return Habit.objects.filter(user=self.request.user)


class HabitCreateView(generics.CreateAPIView):
    """Контроллер создания привычки"""
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        """Привязываем текущего пользователя к создаваемому объекту"""
        new_habit = serializer.save()
        new_habit.user = self.request.user
        new_habit.save()


class HabitDetailView(generics.RetrieveAPIView):
    """Контроллер просмотра привычки"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwner]


class HabitUpdateView(generics.UpdateAPIView):
    """Контроллер редактирования привычки"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwner]


class HabitDeleteView(generics.DestroyAPIView):
    """Контроллер удаления привычки"""
    queryset = Habit.objects.all()
    permission_classes = [IsOwner]