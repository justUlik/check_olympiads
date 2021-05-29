"""
Functions for query processing of olympiads app
"""
from django.shortcuts import render
from .models import Olympiad, registerOlympiad
from autorization.models import Profile
from django.contrib.auth.decorators import login_required

def check_olympiad_info(request, olympiad_name):
    """
    Rendering html template for showing information about each olympiad
    """
    olympiad = Olympiad.objects.get(name=olympiad_name)
    context = {'name': olympiad.name,
               'subject': olympiad.subject,
               'description' : olympiad.description,
               'register_end_date': olympiad.register_end_date,
               'rank': olympiad.rank}
    return render(request, 'olympiads/olympiad_info.html', context=context)

@login_required(login_url='../signin/')
def register_to_olympiad(request, olympiad_name):
    olympiad = Olympiad.objects.get(name=olympiad_name)
    usr = request.user
    profile = Profile.objects.get(user=usr)
    try:
        register_to = registerOlympiad(olympiad=olympiad, usr=usr, usr_profile=profile)
        register_to.save()
        return render(request, "olympiads/success_register.html", context={'name': olympiad.name,
                   'subject': olympiad.subject,
                   'description' : olympiad.description,
                   'register_end_date': olympiad.register_end_date,
                   'rank': olympiad.rank,
                   'competition_date': olympiad.competition_date})
    except:
        return render(request, "olympiads/success_register.html", context={'name': olympiad.name,
                   'subject': olympiad.subject,
                   'description' : olympiad.description,
                   'register_end_date': olympiad.register_end_date,
                   'rank': olympiad.rank,
                   'competition_date': olympiad.competition_date,
                   'address': olympiad.address})
