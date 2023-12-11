from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import UserWord
from datetime import date
from langy import settings
from .utils import get_new_word_to_learn
from .serializers import ExerciseSerializer


class ExerciseView(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        queryset = UserWord.objects.filter(day_to_repeat=date.today())

        # queryset = UserWord.objects.filter(user=user, day_to_repeat=date.today())
        if len(queryset) < settings.NUMBER_OF_WORDS_SESSION:
            queryset = get_new_word_to_learn(user_word=queryset)

        serializer = ExerciseSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
