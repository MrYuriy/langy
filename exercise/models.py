from django.db import models
from langy import settings
from datetime import date, timedelta
from django.utils import timezone


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
    DAY_REPEAT_LEVEL = (
        (1, '1'),
        (3, '3'),
        (5, '5'),
        (7, '7'),
        (30, '30')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    native_word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name="native_word")
    day_to_repeat = models.DateField(default=timezone.now, blank=True)
    status = models.BooleanField(default=False)
    day_repeat_level = models.IntegerField(choices=DAY_REPEAT_LEVEL, default=1)

    def increase_repeat_level(self):
        # Find the index of the current day_repeat_level in DAY_REPEAT_LEVEL
        print(self.day_repeat_level)
        current_index = next(
            (i for i, v in enumerate(self.DAY_REPEAT_LEVEL) if v[1] == self.day_repeat_level), None)
        if current_index is None:
            current_index = 0

        if current_index < len(self.DAY_REPEAT_LEVEL) - 1:
            # Increase day_repeat_level by the value of the next level in DAY_REPEAT_LEVEL
            next_level_value = self.DAY_REPEAT_LEVEL[current_index + 1][1]
            self.day_repeat_level = int(next_level_value)
            self.day_to_repeat = date.today() + timedelta(days=int(next_level_value))
            self.save()
            print("After save", self.day_to_repeat, self.day_repeat_level)
        else:
            self.status = True

    def reduce_repeat_level(self):
        self.day_repeat_level = 1
        self.day_repeat = date.today() + timedelta(days=1)
        self.save()

    def __str__(self):
        return self.word.name
