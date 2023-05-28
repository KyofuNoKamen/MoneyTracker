import json
from base64 import b64encode

import requests
from PIL import Image
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .forms import SignUpForm, IncomeAddingForm, SpendingAddingForm, ProfileForm, ProfileImageForm
from .models import Income, Spending, Account, Saving
from .serializers import UserSerializer, IncomeSerializer

import xlwt


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.error(request, "There Was An Error Logging In. PLease Try Again...")
            return redirect('login')

    else:
        return render(request, "login.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out!")
    return redirect('login')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # second_name = form.cleaned_data['second_name']
            # email = form.cleaned_data['email']
            # Log in User
            user = authenticate(username=username, password=password)
            login(request, user)
            account = Account.objects.create(user=user)
            messages.success(request, "You have successfully registered! Welcome!")
            return redirect('home')

    return render(request, "register.html", {'form': form})


def home(request):
    user = request.user
    incomes = {}
    sumIncomes = 0
    for obj in Income.objects.filter(user=user):
        if incomes.get(obj.category):
            incomes[obj.category] += obj.amount
        else:
            incomes[obj.category] = obj.amount
        sumIncomes += obj.amount

    spending = {}
    sumSpending = 0
    for obj in Spending.objects.filter(user=user):
        if spending.get(obj.category):
            spending[obj.category] += obj.amount
        else:
            spending[obj.category] = obj.amount
        sumSpending += obj.amount

    account = Account.objects.filter(user=user).first()
    if account:
        if account.image:
            image = account.image.url
            imageSplit = image.split('/')
            image = 'images/' + imageSplit[4]
        else:
            image = ''

    temp_today = {}
    for obj in Spending.objects.filter(user=user):
        if obj.time.day - timezone.now().day == 0:
            if temp_today.get(obj.time.hour + 3):
                temp_today[obj.time.hour + 3] += obj.amount
            else:
                temp_today[obj.time.hour + 3] = obj.amount

    today = {'02:00': 0, '04:00': 0, '06:00': 0, '08:00': 0, '10:00': 0, '12:00': 0, '14:00': 0, '16:00': 0, '18:00': 0, '20:00': 0, '22:00': 0, '24:00': 0}
    for key, value in temp_today.items():
        if 0 < key < 2:
            today['02:00'] += value
        elif 2 < key < 4:
            today['04:00'] += value
        elif 4 < key < 6:
            today['06:00'] += value
        elif 6 < key < 8:
            today['08:00'] += value
        elif 8 < key < 10:
            today['10:00'] += value
        elif 10 < key < 12:
            today['12:00'] += value
        elif 12 < key < 14:
            today['14:00'] += value
        elif 14 < key < 16:
            today['16:00'] += value
        elif 16 < key < 18:
            today['18:00'] += value
        elif 18 < key < 20:
            today['20:00'] += value
        elif 20 < key < 22:
            today['22:00'] += value
        elif 22 < key < 24:
            today['24:00'] += value

    savings = {}
    sumSavings = 0
    for obj in Saving.objects.filter(user=user):
        if savings.get(obj.category):
            savings[obj.category] += obj.amount
        else:
            savings[obj.category] = obj.amount
        sumSavings += obj.amount



    req = requests.get('https://bank.gov.ua/NBUStatService/v1/statdirectory/exchangenew?json').text

    req_info = json.loads(req)

    exchange = {}

    for i in range(len(req_info)):
        if req_info[i]['cc'] == 'USD':
            exchange[req_info[i]['cc']] = req_info[i]['rate']
        elif req_info[i]['cc'] == 'EUR':
            exchange[req_info[i]['cc']] = req_info[i]['rate']
        elif req_info[i]['cc'] == 'AUD':
            exchange[req_info[i]['cc']] = req_info[i]['rate']
        elif req_info[i]['cc'] == 'CAD':
            exchange[req_info[i]['cc']] = req_info[i]['rate']
        elif req_info[i]['cc'] == 'JPY':
            exchange[req_info[i]['cc']] = req_info[i]['rate']
        elif req_info[i]['cc'] == 'CHF':
            exchange[req_info[i]['cc']] = req_info[i]['rate']



    context = {
        'user': user,
        'incomes': incomes,
        'sumIncomes': sumIncomes,
        'spending': spending,
        'sumSpending': sumSpending,
        'randomList': range(0, 255, 1),
        'image': image,
        'today': today,
        'savings': savings,
        'sumSavings': sumSavings,
        'exchange': exchange,
    }

    return render(request, "home.html", context)


def adding(request):
    user = request.user
    incomeForm = IncomeAddingForm()
    spendingForm = SpendingAddingForm()

    if request.method == "POST":
        if 'income' in request.POST:
            incomeForm = IncomeAddingForm(request.POST)
            if incomeForm.is_valid():
                amount = incomeForm.cleaned_data['amount']
                time = incomeForm.cleaned_data['time']
                category = incomeForm.cleaned_data['category']
                paymentMethod = incomeForm.cleaned_data['paymentMethod']

                Income.objects.create(user=user, amount=amount, time=time, category=category,
                                      paymentMethod=paymentMethod)
                messages.success(request, "You have successfully added Income!")
                return redirect('adding')

        elif 'spending' in request.POST:
            if request.method == "POST":
                spendingForm = SpendingAddingForm(request.POST)
                if spendingForm.is_valid():
                    amount = spendingForm.cleaned_data['amount']
                    time = spendingForm.cleaned_data['time']
                    category = spendingForm.cleaned_data['category']
                    paymentMethod = spendingForm.cleaned_data['paymentMethod']

                    Spending.objects.create(user=user, amount=amount, time=time, category=category,
                                            paymentMethod=paymentMethod)
                    messages.success(request, "You have successfully added Spending!")
                    return redirect('adding')

    account = Account.objects.filter(user=user).first()
    if account:
        if account.image:
            image = account.image.url
            imageSplit = image.split('/')
            image = 'images/' + imageSplit[4]
        else:
            image = ''

    context = {
        'user': user,
        'incomeForm': incomeForm,
        'spendForm': spendingForm,
        'incomes': Income.objects.filter(user=user),
        'spending': Spending.objects.filter(user=user),
        'image': image,
    }

    return render(request, "adding.html", context)


def profile(request):
    user = request.user
    account = Account.objects.filter(user=user).first()
    profileForm = ProfileForm()
    profileImageForm = ProfileImageForm()
    profileForm.default_settings(firstName=user.first_name, lastName=user.last_name, email=user.email)
    if request.method == "POST":
        if 'profile' in request.POST:
            profileForm = ProfileForm(request.POST)
            if profileForm.is_valid():
                user.first_name = profileForm.cleaned_data['first_name']
                user.last_name = profileForm.cleaned_data['last_name']
                user.email = profileForm.cleaned_data['email']

                messages.success(request, "You have successfully changed Profile!")
                return redirect('profile')

        elif 'image' in request.POST:
            profileImageForm = ProfileImageForm(request.POST, request.FILES)
            if profileImageForm.is_valid():
                account.image = profileImageForm.cleaned_data.get("image")
                account.save()
                messages.success(request, "You have successfully changed Image!")
                return redirect('profile')

    if account:
        if account.image:
            image = account.image.url
            imageSplit = image.split('/')
            image = 'images/' + imageSplit[4]
        else:
            image = ''

    context = {
        'user': user,
        'profileForm': profileForm,
        'profileImageForm': profileImageForm,
        'image': image
    }

    return render(request, "profile.html", context)


def export(request):
    user = request.user
    account = Account.objects.filter(user=user).first()

    if account.image:
        image = account.image.url
        imageSplit = image.split('/')
        image = 'images/' + imageSplit[4]
    else:
        image = ''

    context = {
        'image': image
    }

    return render(request, "export.html", context)


def export_income_xls(request):
    user = request.user

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="includes.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Includes Data')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['amount', 'category', 'paymentMethod']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = Income.objects.filter(user=user).values_list('amount', 'category', 'paymentMethod')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response

