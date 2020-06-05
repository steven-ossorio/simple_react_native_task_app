from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from authentication.models import User
from tasks.models import Tasks
from django.contrib.auth.hashers import make_password, check_password
import json
import jwt
from datetime import datetime, timedelta, time
from django.core import serializers


@csrf_exempt
def index(request):
    response = json.loads(request.body)
    token = response['token']
    user_id = jwt.decode(token, 'secret',
                         algorithm='HS256')['user_id']
    u = User.objects.get(id=user_id)

    today = datetime.now().date()

    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())
    tasks = Tasks.objects.filter(
        task_date__lte=today_end, task_date__gte=today_start).filter(owner=u)
    serialized_queryset = serializers.serialize('python', tasks)
    return JsonResponse(serialized_queryset, safe=False)


@csrf_exempt
def login(request):
    response_dict = json.loads(request.body)
    email = response_dict['email']
    password = response_dict['password']
    if is_email_not_valid(email) or is_password_not_valid(password):
        message = 'Either email or password are incorrect.'
        response = JsonResponse({'status': False, 'message': message})
        response.status_code = 400
        return response

    u = User.objects.get(email=email)

    token = jwt.encode({'user_id': u.id}, 'secret',
                       algorithm='HS256')

    data = {
        'token': token.decode('utf-8'),
        'user_id': u.id
    }

    return JsonResponse(data)


@csrf_exempt
def signup(request):
    response_dict = json.loads(request.body)
    email = response_dict['email']
    password = response_dict['password']
    hashed_password = make_password(password)
    if is_email_not_valid(email) or is_password_not_valid(password):
        message = 'Either email or password are incorrect.'
        response = JsonResponse({'status': False, 'message': message})
        response.status_code = 400
        return response

    u = User(email=email, password=hashed_password)
    u.save()

    token = jwt.encode({'user_id': u.id}, 'secret',
                       algorithm='HS256')

    data = {
        'token': token.decode('utf-8'),
        'user_id': u.id
    }

    return JsonResponse(data)


@csrf_exempt
def create_task(request):
    response = json.loads(request.body)
    title = response['title']
    description = response['description']
    task_date = response['date']
    token = response['token']
    print(token)
    user_id = jwt.decode(token, 'secret',
                         algorithm='HS256')['user_id']
    u = User.objects.get(id=user_id)
    t = Tasks(title=title, description=description,
              task_date=task_date, owner=u)
    t.save()

    newTask = Tasks.objects.filter(id=t.id)

    serialized_queryset = serializers.serialize('python', newTask)
    return JsonResponse(serialized_queryset, safe=False)


@csrf_exempt
def delete_task(request):
    response = json.loads(request.body)
    task_id = response['id']

    Tasks.objects.get(id=task_id).delete()

    return JsonResponse({'task_id': task_id})


@csrf_exempt
def update_task(request):
    response = json.loads(request.body)
    task_id = response['id']
    title = response['title']
    description = response['description']
    task_date = response['date']

    task = Tasks.objects.get(id=task_id)
    task.title = title
    task.description = description
    task.task_date = task_date
    task.save()

    task = Tasks.objects.filter(id=task_id)

    serialized_queryset = serializers.serialize('python', task)
    return JsonResponse(serialized_queryset, safe=False)


@csrf_exempt
def update_account(request):
    response = json.loads(request.body)
    current_password = response['currentPassword']
    new_password = response['newPassword']
    token = response['token']
    user_id = jwt.decode(token, 'secret',
                         algorithm='HS256')['user_id']

    u = User.objects.get(id=user_id)
    if check_password(current_password, u.password):
        u.password = make_password(new_password)
        u.save()

    return JsonResponse({"success": True})

# Conditions we want to be met for authentication purpose


def is_email_not_valid(email):
    return is_empty(email)


def is_password_not_valid(password):
    return is_empty(password)


def is_empty(value):
    return value == ""
