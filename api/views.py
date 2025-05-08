from rest_framework import viewsets, permissions
from .serializers import ChallengeSerializer, EntrySerializer
from challenges.models import Challenge
from entries.models    import Entry

class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.select_related('challenge','user')
    serializer_class = EntrySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

