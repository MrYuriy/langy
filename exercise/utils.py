from .models import Word, UserWord, Dictionary, Language
from django.contrib.auth import get_user_model
from datetime import date
import random


def get_missing_word(dictionary, user_known_words, count_word_to_return):
    result_items = []
    
    for learn_word, native_word in  random.sample(dictionary.items(), len(dictionary.items())):
        if learn_word not in user_known_words:
            result_items.append((learn_word, native_word))
            if len(result_items) == count_word_to_return:
                break
    return result_items


def get_new_word_to_learn(count_words, user_word, user):
    
    learning_language = Language.objects.get(name=user.learn_language)
    native_language = Language.objects.get(name=user.native_language)
    

    user_known_words = user_word.values_list("word__name", flat=True)
    dictionary = Dictionary.objects.get(name=user.learn_language).dictionary
    count_word_to_return = count_words - len(user_word)
    
    result_items = get_missing_word(
        dictionary=dictionary,
        user_known_words=user_known_words,
        count_word_to_return=count_word_to_return
    )
    #print(result_items)

    eng_words = [Word(name=learn_le, language=learning_language) for learn_le, nat_le in result_items]
    ua_words = [Word(name=nat_le, language=native_language) for learn_le, nat_le in result_items]

    Word.objects.bulk_create(
        eng_words + ua_words
    )

    eng_words = Word.objects.filter(name__in=[word.name for word in eng_words])
    ua_words = Word.objects.filter(name__in=[word.name for word in ua_words])

    user_word_to_create = [
        UserWord(
            user=user,
            word=learn_le,
            native_word=nat_le,
        )
        for learn_le, nat_le in zip(eng_words, ua_words)
    ]
    
    UserWord.objects.bulk_create(user_word_to_create)
    user_word = list(user_word)
    user_word += user_word_to_create
    return user_word
