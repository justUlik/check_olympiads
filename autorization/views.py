"""
Functions for query processing of autorization app
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.db import transaction
from .models import Profile
from .forms import ProfileForm
from olympiads.filters import OlympiadFilter
from olympiads.models import Olympiad, registerOlympiad
import datetime


def login_view(request):
    """
    Sign in providing, rendering an html template
    """
    next = request.GET.get('next')
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            if next:
                return redirect(next)
            return redirect('/')
        return render(request, 'autorization/signinFailed.html', context={'form' : UserLoginForm()})

    return render(request, 'autorization/signin.html', context={'form' : UserLoginForm()})


def logout_view(request):
    """
    Logout
    """
    logout(request)
    return redirect('/')


def register_view(request):
    """
    Sign out providing, rendering an html template
    """
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        #email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        user = authenticate(username=user.username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')
    elif request.method == "POST":
        return render(request, 'autorization/signupFailed.html')

    context = {
        'form': form,
    }
    return render(request, 'autorization/signup.html', context)

@login_required(login_url='../signin/')
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    olympiads = registerOlympiad.objects.filter(usr=request.user)
    data_olympiads = []
    for olympiad in olympiads:
        if olympiad.olympiad.register_end_date >= datetime.date.today() and olympiad.olympiad.competition_date >= datetime.date.today():
            data_olympiads.append(olympiad.olympiad)
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            if profile_form.cleaned_data['first_name']:
                profile.first_name = profile_form.cleaned_data['first_name']
                profile.save(update_fields=["first_name"])
            if profile_form.cleaned_data['second_name']:
                profile.second_name = profile_form.cleaned_data['second_name']
                profile.save(update_fields=["second_name"])
            if profile_form.cleaned_data['father_name']:
                profile.father_name = profile_form.cleaned_data['father_name']
                profile.save(update_fields=["father_name"])
            if profile_form.cleaned_data['grade']:
                profile.grade = profile_form.cleaned_data['grade']
                profile.save(update_fields=["grade"])
            if profile_form.cleaned_data['birth_date']:
                profile.birth_date = profile_form.cleaned_data['birth_date']
                profile.save(update_fields=["birth_date"])
            messages.success(
                request, ('Профиль успешно обновлен'))
            return HttpResponseRedirect('/autorization/profile/')
        else:
            messages.error(request, ('Были введены данные в некорректном формате'))
    else:
        profile_form=ProfileForm(instance=request.user.profile)
    return render(request,'autorization/userprofile_upd.html',
							  {"email" : profile.user.email,
							   "username" : profile.user.username,
							   "first_name": profile.first_name,
							   "second_name": profile.second_name,
							   "father_name": profile.father_name,
							   "grade": profile.grade,
                               "birth_date": profile.birth_date,
                               'profile_form': profile_form,
                               'data_olympiads' : data_olympiads,
                               'len': len(data_olympiads)})
