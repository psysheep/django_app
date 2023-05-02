from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from library.forms import ReviewForm
from library.methods.book_reader import check_reviewed
from library.models import Book
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


class LeaveReview(LoginRequiredMixin, generic.View):
    login_url = 'user:login'
    template_name = 'add_review.html'

    def get(self, request, book_pk):
        existing_review = check_reviewed(request.user.pk, book_pk)
        form = ReviewForm(instance=existing_review) if existing_review else ReviewForm()
        book = Book.objects.get(pk=book_pk)
        return render(request, self.template_name, {'form': form, 'book': book, 'reviewed': bool(existing_review)})

    def post(self, request, book_pk):
        existing_review = check_reviewed(request.user.pk, book_pk)
        form = ReviewForm(request.POST, instance=existing_review)
        book = Book.objects.get(pk=book_pk)
        if 'delete' in request.POST:
            existing_review.delete()
            return redirect('library:book', pk=book.pk)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect('library:book', pk=book.pk)
        return render(request, self.template_name, {'form': form, 'book': book})
