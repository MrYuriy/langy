from django.db import models
from langy import settings
from datetime import date


class Language(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Dictionary(models.Model):
    name = models.CharField(max_length=10)
    dictionary = models.JSONField()

    def __str__(self):
        return self.language


class Word(models.Model):

    name = models.CharField(max_length=20)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    false_answer_count = models.IntegerField(default=0)
    true_answer_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class UserWord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    native_word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name="native_word")
    day_to_repeat = models.DateField(blank=date.today())
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.word.name
