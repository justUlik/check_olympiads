"""
Functions for query processing of mainpage app
"""

from django.shortcuts import render
from olympiads.models import Olympiad, registerOlympiad
from olympiads.filters import OlympiadFilter
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
    filter = OlympiadFilter(request.GET, queryset=olympiads)
    olympiads = filter.qs
    if request.user.is_authenticated:
        res = []
        for olympiad in olympiads:
            now = registerOlympiad.objects.filter(olympiad=olympiad, usr=request.user)
            if len(now) == 0:
                res.append(olympiad)
        olympiads = res
    subjects = ['Математика', 'Русский язык', 'Литература', 'История', 'Физическая культура', 'Музыка', 'Технология', 'Химия', 'Биология', 'Физика', 'Экология', 'География', 'Естествознание', 'Астрономия', 'Окружающий мир', 'Изобразительное искусство', 'Основы безопасности жизнедеятельности', 'Информатика', 'Робототехника', 'Экономика']
    ranks = ['1', '2', '3', 'нет']
    grades = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
    for olympiad in olympiads:
        day = olympiad.register_end_date - datetime.date.today()
        day = _plural_days(day.days)
        data.append([
            olympiad.subject,
            olympiad.name,
            day,
            olympiad.grade,
            olympiad.rank])
    if request.user_agent.is_mobile:
        return render(request, 'mainpage/mobile/index.html', {'data': data, 'subjects' : subjects, 'ranks' : ranks, 'grades': grades, 'len': len(data)})
    else:
        return render(request, 'mainpage/index.html', {'data': data, 'subjects' : subjects, 'ranks' : ranks, 'grades': grades, 'len': len(data)})    
