from django.urls import path
from .views import EntryListView, EntryCreateView, EntryDetailView, EntryUpdateView, EntryDeleteView

app_name = 'entries'

urlpatterns = [
    path('', EntryListView.as_view(), name='list'),
    path('add/<slug:slug>/', EntryCreateView.as_view(), name='add'),
    path('<int:pk>/', EntryDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', EntryUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', EntryDeleteView.as_view(), name='delete'),
]
