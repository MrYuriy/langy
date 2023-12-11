from django.urls import path
from .views import ExerciseView

urlpatterns = [
    path("cards/", ExerciseView.as_view(), name="cards"),
]

app_name = "exercise"
