from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import login
from django.contrib import messages


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
