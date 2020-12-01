from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    avatar = models.ImageField()
    date_create = models.DateField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


# class TagManager(models.Manager):
#     def questions_with_tag(self):
#         return Question.objects.filter(pk=)


class Tag(models.Model):
    title = models.CharField(max_length=50)

    # objects = TagManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class QuestionManager(models.Manager):
    def published_new(self):
        return self.order_by('-date_create')

    def published_best(self):
        return self.order_by('-rating')

    def question_with_tag(self, tag):
        return self.filter(tags=tag)


class Question(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_create = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    rating = models.IntegerField(default=0)

    objects = QuestionManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class AnswerManager(models.Manager):
    def answers_for_question(self, pk):
        return self.filter(question=Question.objects.get(id=pk))

    def count_answers(self, question):
        return self.filter(question=question).count()


class Answer(models.Model):
    text = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_create = models.DateField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    objects = AnswerManager()


class MarkForQuestions(models.Model):
    is_like = models.BooleanField(default=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.is_like

    class Meta:
        verbose_name = 'MarkForQuestion'
        verbose_name_plural = 'MarksForQuestions'


class MarkForAnswers(models.Model):
    is_like = models.BooleanField(default=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.is_like

    class Meta:
        verbose_name = 'MarkForAnswer'
        verbose_name_plural = 'MarksForAnswers'
