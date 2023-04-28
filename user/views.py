from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RegistrationForm
from .models import Review, ReadingProgress


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'You have been Signed Up!')
            return redirect('library:books')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


class UserDetails(LoginRequiredMixin, generic.DetailView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'user_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_reviews'] = Review.objects.filter(user=self.object)
        context['reading_progress'] = ReadingProgress.objects.filter(user=self.object)
        return context
