from django.db import models
from langy import settings
from datetime import date


class Language(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Dictionary(models.Model):
    DIFFICULT_LEVEL_CHOICES = (
        ("Easy", "Easy"),
        ("Middle", "Middle"),
        ("Hard", "Hard"),
    )

    language = models.CharField(max_length=10)
    difficulty_level = models.CharField(max_length=6, choices=DIFFICULT_LEVEL_CHOICES)
    dictionary = models.JSONField()

    def __str__(self):
        return self.language


class Word(models.Model):
    DIFFICULT_LEVEL_CHOICES = (
        ("Eazy", "Eazy"),
        ("Middle", "Middle"),
        ("Hard", "Hard"),
    )

    name = models.CharField(max_length=20)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    difficulty_level = models.CharField(max_length=6, choices=DIFFICULT_LEVEL_CHOICES)

    def __str__(self):
        return self.name


class UserWord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    native_word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name="native_word")
    day_to_repeat = models.DateField(auto_now=date.today(), blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.word.name
