"""
Functions for query processing of mainpage app
"""

from django.shortcuts import render
from olympiads.models import Olympiad
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

def view_olympiads(request):
    """
    Function for processing data of all Olympiad objects
    and rendering an html template of mainpage
    """
    data = []
    olympiads = Olympiad.objects.filter(register_end_date__gte=datetime.date.today()).order_by('register_end_date')
    for olympiad in olympiads:
        day = olympiad.register_end_date - datetime.date.today()
        day = _plural_days(day.days)
        data.append([
            olympiad.subject,
            olympiad.name,
            day,
            olympiad.rank])
    return render(request, 'mainpage/index.html', {'data': data})
