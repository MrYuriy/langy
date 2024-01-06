from django.contrib import admin
from .models import Language, Word, UserWord, Dictionary


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ("name", "language", "false_answer_count", "true_answer_count")
    list_filter = ("name", "language", "false_answer_count", "true_answer_count")


@admin.register(UserWord)
class UserWordAdmin(admin.ModelAdmin):
    list_display = ("user", "word", "native_word", "day_to_repeat", "day_repeat_level", "status")
    list_filter = ("user", "status")

@admin.register(Dictionary)
class DictionaryAdmin(admin.ModelAdmin):
    list_filter = ("name",)
