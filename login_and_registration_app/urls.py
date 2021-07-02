from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('users/register', views.register),
    path('users/login', views.login),
    # path('users/success', views.success),
    path('users/logout', views.logout),
    path('exercises', views.exercises),
    path('my_account/<int:id>', views.my_account),
    path('add_exercises', views.add_exercises),
    path('like/<int:id>', views.add_like),
    path('delete_exercise/<int:id>', views.delete_exercise),
    path('edit/<int:id>', views.edit_user),
    path('profile/<int:id>', views.profile),
    path('workouts', views.workouts),
    path('workout/assign', views.add_workout),
    path('delete_workout/<int:id>', views.delete_workout),
    path('workout/<int:workout_id>', views.edit_workout),
    path('workout/<int:workout_id>/assign', views.assign_exercise),
    path('remove_exercise/<int:exercise_id>/<int:workout_id>', views.remove_exercise),
]
