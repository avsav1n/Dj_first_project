from django.http import HttpResponse
from django.shortcuts import render, reverse

from datetime import datetime
import os
import re


def home_view(request):
    template_name = 'app/home.html'
    # впишите правильные адреса страниц, используя
    # функцию `reverse`
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }
    
    # context и параметры render менять не нужно
    # подбробнее о них мы поговорим на следующих лекциях
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    # обратите внимание – здесь HTML шаблона нет, 
    # возвращается просто текст
    current_time = datetime.now().time().strftime('%H:%M:%S')
    msg = f'Текущее время: {current_time}'
    return HttpResponse(msg)


def workdir_view(request):
    # по аналогии с `time_view`, напишите код,
    # который возвращает список файлов в рабочей 
    # директории
    dir_tree = '<pre>'
    startpath = os.getcwd()
    for root, dirs, files in os.walk(startpath):
        if re.search('.venv|.vscode|.git|__pycache__', root):
            continue
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        # dir_tree += f'<p style="text-indent: {5 * len(indent)}px;">{os.path.basename(root)}/</p>'
        dir_tree += f'{indent}{os.path.basename(root)}/\n'


        subindent = ' ' * 4 * (level + 1)
        for f in files:
            dir_tree += f'{subindent}{f}\n'
    dir_tree += '</pre>'

    return HttpResponse(dir_tree)
