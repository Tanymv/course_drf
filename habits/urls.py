from django.urls import path

from habits.apps import HabitsConfig
from habits.views import HabitListView, HabitCreateView, HabitDetailView, HabitUpdateView, HabitDeleteView, \
    UserHabitListView

app_name = HabitsConfig.name

urlpatterns = [
    path('', HabitListView.as_view(), name='habit_list'),
    path('my/', UserHabitListView.as_view(), name='my_habit_list'),
    path('create/', HabitCreateView.as_view(), name='habit_create'),
    path('<int:pk>/', HabitDetailView.as_view(), name='habit_view'),
    path('update/<int:pk>/', HabitUpdateView.as_view(), name='habit_update'),
    path('delete/<int:pk>/', HabitDeleteView.as_view(), name='habit_delete'),
]