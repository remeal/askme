from django.contrib import admin
from app.models import Question, Tag, Answer, Profile, MarkForAnswers, MarkForQuestions

admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(Answer)
admin.site.register(Profile)
admin.site.register(MarkForQuestions)
admin.site.register(MarkForAnswers)
