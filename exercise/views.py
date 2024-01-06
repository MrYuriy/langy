from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import UserWord
from datetime import date, datetime, timedelta
from langy import settings
from .utils import get_new_word_to_learn
from .serializers import GetCardSerializer, AnalizAnswerSerializer
from django.contrib.auth import get_user_model


class ExerciseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        queryset = UserWord.objects.filter(user=user, day_to_repeat__lte=date.today())
        count_words = int(request.query_params.get("count-words", settings.NUMBER_OF_WORDS_SESSION))

        if len(queryset) < count_words:
            queryset = get_new_word_to_learn(count_words, user_word=queryset)
        else:
            queryset = queryset[:count_words]
        serializer = GetCardSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        data = self.request.data
        serializer = AnalizAnswerSerializer(data=data)

        if serializer.is_valid():
            user_word = UserWord.objects.filter(user=user, word__id=data["id"])[0]
            if data["status"]:
                user_word.increase_repeat_level()
            else:
                user_word.reduce_repeat_level()

            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
