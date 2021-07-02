from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
import re

def index(request):
    return render(request, 'index.html')

def register(request):
    pw_hash=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    errors=User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ('/')
    else:
        user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=pw_hash,
        )
        request.session['user_id']=user.id
        request.session['user_first_name']=user.first_name
        request.session['user_last_name']=user.last_name
        request.session['user_email']=user.email
        return redirect('/exercises')

def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user=user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id']=logged_user.id
            request.session['user_first_name']=logged_user.first_name
            request.session['user_last_name']=logged_user.last_name
            request.session['user_email']=logged_user.email
            return redirect('/exercises')
        else:
            messages.error(request, "Incorrect email and/or password.")
            return redirect('/')
    else:
            messages.error(request, "Incorrect email and/or password.")
            return redirect('/')

# def success(request):
#     if 'user_id' not in request.session:
#         return redirect('/')
#     user = User.objects.get(id=request.session['user_id'])
#     context = {
#         'user':user
#     }
#     return render(request, 'exercises.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

def exercises(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'exercises': Exercise.objects.all(),
    }
    return render(request, 'exercises.html', context)

def add_exercises(request):
    errors=Exercise.objects.exercise_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ('/exercises')
    exercise = Exercise.objects.create(
        name=request.POST['name'],
        muscle_group=request.POST['muscle_group'],
        equipment=request.POST['equipment'],
        user=User.objects.get(id=request.session['user_id'])
)
    return redirect('/exercises')

def add_like(request, id):
    liked_exercise=Exercise.objects.get(id=id)
    user=User.objects.get(id=request.session['user_id'])
    liked_exercise.likes.add(user)
    return redirect('/exercises')

def delete_exercise(request, id):
    exercise_to_delete= Exercise.objects.get(id=id)
    exercise_to_delete.delete()
    return redirect('/exercises')

def my_account(request, id):
    context = {
        'user': User.objects.get(id=id)
    }
    return render(request, 'my_account.html', context)

def edit_user(request, id):
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if len(request.POST['first_name']) > 2:
        if len(request.POST['last_name']) > 2:
            edit_user = User.objects.get(id=id)
            if request.POST['email'] != edit_user.email:
                email=User.objects.filter(email=request.POST['email'])
                if len(request.POST['email']) > 0:
                    if len(email) <= 0:
                        if not EMAIL_REGEX.match(request.POST['email']):
                            messages.error(request,'Invalid Email address')
                        else:
                            edit_user.first_name = request.POST['first_name']
                            edit_user.last_name = request.POST['last_name']
                            edit_user.email = request.POST['email']
                            edit_user.save()
                            messages.success(request, "You have successfully updated your account")
                    else:
                        messages.error(request, 'This email already exists')
                else:
                    messages.error(request, 'Email is required')
            else:
                edit_user.first_name = request.POST['first_name']
                edit_user.last_name = request.POST['last_name']
                edit_user.email = request.POST['email']
                edit_user.save()
                messages.success(request, "You have successfully updated your account")
        else:
            messages.error(request, 'Last name must be at least 2 characters')
    else:
        messages.error(request, 'First name must be at least 2 characters')
    return redirect(f'/my_account/{id}')

def profile(request, id):
    context = {
        'profile_exercises': Exercise.objects.filter(user_id=id),
        'user': User.objects.get(id=id),
    }
    return render(request, 'profile.html', context)

def workouts(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'exercises': Exercise.objects.all(),
        'workouts': Workout.objects.all(),
    }
    return render(request, 'workouts.html', context)


def add_workout(request):
    errors=Workout.objects.workout_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ('/workouts')
    workout = Workout.objects.create(
        name=request.POST['name'],
        description=request.POST['description'],
        user=User.objects.get(id=request.session['user_id'])
)
    return redirect('/workouts')

def delete_workout(request, id):
    workout_to_delete= Workout.objects.get(id=id)
    workout_to_delete.delete()
    return redirect('/workouts')

def edit_workout(request, workout_id):
    workout = Workout.objects.get(id=workout_id)
    context = {
        'workout': workout,
        'exercises': Exercise.objects.all(),
        # 'exercises': Exercise.objects.exclude(workout__id=workout_id)
    }
    return render(request, 'edit_workout.html', context)

def assign_exercise(request, workout_id):
    workout = Workout.objects.get(id=workout_id)
    exercise = Exercise.objects.get(id=request.POST['exercise_id'])
    workout.exercise.add(exercise)
    return redirect(f'/workout/{workout_id}')

def remove_exercise(request, workout_id, exercise_id):
    workout = Workout.objects.get(id=workout_id)
    exercise_to_delete= Exercise.objects.get(id=exercise_id)
    workout.exercise.remove(exercise_to_delete)
    return redirect(f'/workout/{workout_id}')