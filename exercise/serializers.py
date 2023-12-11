from rest_framework import serializers
from exercise.models import UserWord, Word


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = "__all__"


class WordExerciseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class ExerciseSerializer(serializers.ModelSerializer):
    word = WordExerciseSerializer()
    native_word = serializers.CharField(source="native_word.name", read_only=True)

    class Meta:
        model = UserWord
        fields = ("word", "native_word",)
