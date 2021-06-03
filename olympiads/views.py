"""
Functions for query processing of olympiads app
"""
from django.shortcuts import render
from .models import Olympiad, registerOlympiad
from autorization.models import Profile
from django.contrib.auth.decorators import login_required
import datetime

def _plural_days(n):
    days = ['день', 'дня', 'дней']
    if n == 0:
        return 'сегодня'
    if n % 10 == 1 and n % 100 != 11:
        p = 0
    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
        p = 1
    else:
        p = 2
    return str(n) + ' ' + days[p]

def check_olympiad_info(request, olympiad_name):
    """
    Rendering html template for showing information about each olympiad
    """
    olympiad = Olympiad.objects.get(name=olympiad_name)
    day = olympiad.register_end_date - datetime.date.today()
    day = _plural_days(day.days)
    is_registered = False
    try:
        res = registerOlympiad.objects.filter(olympiad=olympiad).filter(usr=request.user)
        if len(res) != 0:
            is_registered = True
    except:
        is_registered = False
    is_profile_good = False
    is_authenticated = False
    if request.user.is_authenticated:
        is_authenticated = True
        usr = request.user
        profile = Profile.objects.get(user=usr)
        if profile.first_name is not "" and profile.second_name is not "":
            is_profile_good = True
    context = {'name': olympiad.name,
               'subject': olympiad.subject,
               'description' : olympiad.description,
               'register_end_date': day,
               'competition_date': olympiad.competition_date,
               'rank': olympiad.rank,
               'support_email': olympiad.support_email,
               'address': olympiad.address,
               'grade': olympiad.grade,
               'is_authenticated' : is_authenticated,
               'is_profile_good' : is_profile_good}
    if is_registered:
        if request.user_agent.is_mobile:
            return render(request, 'olympiads/mobile/success_register.html', context=context)
        else:
            return render(request, 'olympiads/success_register.html', context=context)
    else:
        if request.user_agent.is_mobile:
            return render(request, 'olympiads/mobile/olympiad_info.html', context=context)
        else:
            return render(request, 'olympiads/olympiad_info.html', context=context)

@login_required(login_url='autorization/signin/')
def register_to_olympiad(request, olympiad_name):
    olympiad = Olympiad.objects.get(name=olympiad_name)
    usr = request.user
    profile = Profile.objects.get(user=usr)
    register_to = registerOlympiad(olympiad=olympiad, usr=usr, usr_profile=profile)
    register_to.save()
    return render(request, "olympiads/success_register.html", context={'name': olympiad.name,
                      'subject': olympiad.subject,
                      'description' : olympiad.description,
                      'register_end_date': olympiad.register_end_date,
                      'rank': olympiad.rank,
                      'competition_date': olympiad.competition_date})
