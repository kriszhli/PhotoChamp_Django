from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Entry, EntryReview
from .forms import EntryForm, EntryReviewForm
from django.db.models import Avg

class EntryListView(ListView):
    model = Entry
    template_name = 'entries/entry_list.html'
    context_object_name = 'entries'
    paginate_by = 12

    def get_queryset(self):
        qs = super().get_queryset()
        challenge_slug = self.request.GET.get('challenge')
        if challenge_slug:
            qs = qs.filter(challenge__slug=challenge_slug)
        return qs

class EntryDetailView(LoginRequiredMixin, DetailView):
    model = Entry
    context_object_name = 'entry'
    template_name = 'entries/entry_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        entry = self.object
        ctx['challenge'] = entry.challenge
        ctx['submitted_at'] = entry.submitted_at
        avg = entry.reviews.aggregate(avg=Avg('rating'))['avg']
        ctx['average_rating'] = round(avg or 0, 2)
        ctx['reviews'] = entry.reviews.all()
        ctx['review_form'] = EntryReviewForm()

        return ctx

class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = EntryForm
    template_name = 'entries/entry_form.html'
    success_url = reverse_lazy('entries:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EntryUpdateView(LoginRequiredMixin, UpdateView):
    model = Entry
    form_class = EntryForm
    template_name = 'entries/entry_form.html'
    success_url = reverse_lazy('entries:list')

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)

class EntryDeleteView(LoginRequiredMixin, DeleteView):
    model = Entry
    template_name = 'entries/entry_confirm_delete.html'
    success_url = reverse_lazy('entries:list')

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)

class EntryReviewCreateView(LoginRequiredMixin, CreateView):
    model = EntryReview
    form_class = EntryReviewForm
    template_name = 'entries/entry_review_form.html'

    def form_valid(self, form):
        entry = Entry.objects.get(pk=self.kwargs['pk'])
        form.instance.entry = entry
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('entries:detail', kwargs={'pk': self.kwargs['pk']})

