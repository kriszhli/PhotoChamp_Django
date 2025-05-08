from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from .models import Challenge
from .forms import ChallengeForm
from django.db.models import Q
import datetime

# Function-based view
def challenge_list(request):
    q = request.GET.get('q', '').strip()
    if q:
        # Filtering queryset
        challenges = Challenge.objects.filter(Q(title__icontains=q) | Q(tags__icontains=q))
    else:
        challenges = Challenge.objects.all()
    challenges = challenges.order_by('end_date')

    today = datetime.date.today()
    for ch in challenges:
        delta = ch.end_date - today
        ch.days_left = max(delta.days, 0)

    # Pagination, 3 per page
    paginator = Paginator(challenges, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'challenges/challenge_list.html', {
        'page_obj': page_obj,
        'q': q,
    })

# Class-based views
class ChallengeDetailView(DetailView):
    model = Challenge
    context_object_name = 'challenge'
    template_name = 'challenges/challenge_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        all_entries = self.object.entries.order_by('-submitted_at')

        # 10 per page
        paginator = Paginator(all_entries, 10)
        page_number = self.request.GET.get('page')
        ctx['entries_page'] = paginator.get_page(page_number)

        return ctx

class ManagerRequiredMixin(UserPassesTestMixin):
    login_url = 'useradmin:login'
    raise_exception = True
    def test_func(self):
        return self.request.user.is_staff

class ChallengeCreateView(LoginRequiredMixin, ManagerRequiredMixin, CreateView):
    model = Challenge
    form_class = ChallengeForm
    template_name = 'challenges/challenge_form.html'
    success_url = reverse_lazy('challenges:list')

class ChallengeUpdateView(LoginRequiredMixin, ManagerRequiredMixin, UpdateView):
    model = Challenge
    form_class = ChallengeForm
    template_name = 'challenges/challenge_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('challenges:list')

class ChallengeDeleteView(LoginRequiredMixin, ManagerRequiredMixin, DeleteView):
    model = Challenge
    template_name = 'challenges/challenge_confirm_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('challenges:list')
