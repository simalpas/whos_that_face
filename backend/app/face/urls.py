from django.urls import path

from app.face.views import HomeView

urlpatterns = [
    path("", HomeView.as_view()),
]
