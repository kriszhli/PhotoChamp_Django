from django.shortcuts       import render, redirect
from django.contrib.auth    import login as django_login, logout as django_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .forms  import RegisterForm, ProfileForm
from .models import UserProfile

def auth_view(request):
    url_name = request.resolver_match.url_name

    if url_name == 'signup':
        register_form = RegisterForm(request.POST or None)
        if request.method == 'POST' and register_form.is_valid():
            user = register_form.save()
            django_login(request, user)
            return redirect('main:home')

        return render(request, 'useradmin/signup.html', {
            'register_form': register_form,
        })

    else:
        login_form = AuthenticationForm(request, data=request.POST or None)
        if request.method == 'POST' and login_form.is_valid():
            user = login_form.get_user()
            django_login(request, user)
            return redirect('main:home')

        return render(request, 'useradmin/login.html', {
            'login_form': login_form,
        })


def logout_view(request):
    django_logout(request)
    return redirect('useradmin:login')


@login_required
def profile_detail_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'useradmin/profile_detail.html', {
        'profile': profile,
    })


@login_required
def profile_update_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    form = ProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=profile
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('useradmin:profile')

    return render(request, 'useradmin/profile_form.html', {
        'form': form,
    })