from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from app.models import Question


tags = [
    {
        'id': idx,
        'title': f'tag {idx}',
    } for idx in range(2)
]


def new_questions(request):
    questions = Question.objects.published_new()
    questions = paginate(request, questions, 10)
    return render(request, 'index.html', {
        'tags': tags,
        'questions': questions
    })


def hot_questions(request):
    questions = Question.objects.published_best()
    questions = paginate(request, questions, 10)
    return render(request, 'hot.html', {
        'tags': tags,
        'questions': questions
    })


def login_page(request):
    return render(request, 'login.html', {})


def settings(request):
    return render(request, 'settings.html', {})


def question(request, pk):
    question = questions[pk]
    return render(request, 'question.html', {})


def tag(request, tag):
    
    return render(request, 'tag.html', {
        'tags': tags,
        'questions': questions,
        'title': tag
    })


def ask(request):
    return render(request, 'ask.html', {})


def signup(request):
    return render(request, 'register.html', {})


def paginate(request, questions, per_page):
    objects_list = questions
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page')
    ques = paginator.get_page(page)
    return ques
