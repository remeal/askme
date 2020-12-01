from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.template.defaulttags import register
from app.models import Question, Tag, Answer, MarkForQuestions, Profile, MarkForAnswers
from app.forms import LoginForm, SignUpForm, AskForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required


def count_answers(questions):
    arr = {}
    for question in questions:
        arr.update({question.id: Answer.objects.count_answers(question)})
    return arr


def count_marks_for_quiz(questions, is_liked):
    arr = {}
    for question in questions:
        arr.update({question.id: MarkForQuestions.objects.filter(question=question, is_like=is_liked).count()})
    return arr


def count_marks_for_answer(answers, is_liked):
    arr = {}
    for answer in answers:
        arr.update({answer.id: MarkForAnswers.objects.filter(answer=answer.id, is_like=is_liked).count()})
    return arr
@register.filter
def get_value(dict, key):
    return dict.get(key)


def new_questions(request):
    questions = Question.objects.published_new()
    questions = paginate(request, questions, 10)
    answers = count_answers(questions)
    like = count_marks_for_quiz(questions, True)
    dislike = count_marks_for_quiz(questions, False)
    return render(request, 'index.html', {
        'items': questions,
        'answers': answers,
        'like': like,
        'dislike': dislike
    })


def hot_questions(request):
    questions = Question.objects.published_best()
    questions = paginate(request, questions, 10)
    answers = count_answers(questions)
    like = count_marks_for_quiz(questions, True)
    dislike = count_marks_for_quiz(questions, False)
    return render(request, 'hot.html', {
        'items': questions,
        'answers': answers,
        'like': like,
        'dislike': dislike
    })


def login_page(request):
    if request.method == 'GET':
        form = LoginForm()
        print("HERE")
    else:
        print("AND HERE")
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                request.session['hello'] = 'world'
                auth.login(request, user)
                return redirect("/")
    return render(request, 'login.html', {
        'form': form
    })


def logout(request):
    auth.logout(request)
    return redirect("/")


def settings(request):
    return render(request, 'settings.html', {})


def question(request, pk):
    question = Question.objects.get(id=pk)
    answers = Answer.objects.answers_for_question(pk)
    answers = paginate(request, answers, 10)
    like = MarkForQuestions.objects.filter(question=question, is_like=True).count()
    dislike = MarkForQuestions.objects.filter(question=question, is_like=False).count()
    answers_like = count_marks_for_answer(answers, True)
    answers_dislike = count_marks_for_answer(answers, False)
    return render(request, 'question.html', {
        "question": question,
        "items": answers,
        "like": like,
        "dislike": dislike,
        "answers_like": answers_like,
        'answers_dislike': answers_dislike
    })


def tag(request, tag):
    questions = Question.objects.question_with_tag(tag)
    questions = paginate(request, questions, 10)
    title = Tag.objects.get(id=tag).title
    answers = count_answers(questions)
    return render(request, 'tag.html', {
        'title': title,
        'questions': questions,
        "answers": answers
    })

@login_required
def ask(request):
    if request.method == 'GET':
        form = AskForm()
    else:
        form = AskForm(data=request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect(reverse('question', kwargs={'pk': question.pk}))
    return render(request, 'ask.html', {
        'form': form
    })


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.username = form.cleaned_data.get('username')
            user.email = form.cleaned_data.get('email')
            profile = Profile.objects.create(user=user)
            password = form.cleaned_data.get('password1')
            user = auth.authenticate(username=user.username, email=user.email, password=password)
            auth.login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {
        "form": form
    })


def paginate(request, questions, per_page):
    objects_list = questions
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page')
    ques = paginator.get_page(page)
    return ques
