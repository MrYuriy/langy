from .models import Word, UserWord, Dictionary, Language
from langy.settings import NUMBER_OF_WORDS_SESSION
from django.contrib.auth import get_user_model
from datetime import date


def get_missing_word(dictionary, native_dictionary, count_word_to_return):
    result_items = []
    for learn_word, native_word in dictionary.items():
        if learn_word not in native_dictionary:
            result_items.append((learn_word, native_word))
            if len(result_items) == count_word_to_return:
                break  # Stop when 10 items are collected
    return result_items


def get_new_word_to_learn(user_word, user=None):
    learning_language = user_word[0].word.language
    ua_language = Language.objects.get(name="Ukrainian")
    User = get_user_model()
    user = User.objects.get(email="admin@gmail.com")

    native_dictionary = user_word.values_list("word__name", flat=True)
    dictionary = Dictionary.objects.get(language="English").dictionary
    count_word_to_return = NUMBER_OF_WORDS_SESSION - len(user_word)
    result_items = get_missing_word(
        dictionary=dictionary,
        native_dictionary=native_dictionary,
        count_word_to_return=count_word_to_return
    )

    eng_words = [Word(name=eng, language=learning_language, difficulty_level="Easy") for eng, ua in result_items]
    ua_words = [Word(name=ua, language=ua_language, difficulty_level="Easy") for eng, ua in result_items]

    Word.objects.bulk_create(
        eng_words + ua_words
    )

    user_word_to_create = [
        UserWord(
            user=user,
            word=eng,
            native_word=ua,
            day_to_repeat=date.today(),
            status=False
        )
        for eng, ua in zip(eng_words, ua_words)
    ]
    user_word = list(user_word)
    user_word += UserWord.objects.bulk_create(user_word_to_create)
    return user_word
