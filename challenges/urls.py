from django.urls import path
from .views import challenge_list, ChallengeCreateView, ChallengeDetailView, ChallengeUpdateView, ChallengeDeleteView

app_name = 'challenges'

urlpatterns = [
    path('', challenge_list, name='list'),
    path('add/', ChallengeCreateView.as_view(), name='add'),
    path('<slug:slug>/', ChallengeDetailView.as_view(), name='detail'),
    path('<slug:slug>/edit/', ChallengeUpdateView.as_view(), name='edit'),
    path('<slug:slug>/delete/', ChallengeDeleteView.as_view(), name='delete'),
]