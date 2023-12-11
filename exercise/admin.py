from django.contrib import admin
from .models import Language, Word, UserWord, Dictionary


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ("name", "difficulty_level")
    list_filter = ("name", "language", "difficulty_level")


@admin.register(UserWord)
class UserWordAdmin(admin.ModelAdmin):
    list_display = ("user", "word", "native_word", "day_to_repeat", "status")
    list_filter = ("user", "status")


@admin.register(Dictionary)
class DictionaryAdmin(admin.ModelAdmin):
    list_filter = ("language", )
