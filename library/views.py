from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

from .methods.book_reader import view_single_page
from .models import Book, Review
from .forms import ReviewForm


class BookDetail(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all()
        context['average_rating'] = self.object.reviews.aggregate(Avg('rating'))['rating__avg']
        return context


class BookList(generic.ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'book'


@login_required(login_url='user:login')
def pdf_page_view(request, book_pk, page_number):
    page = view_single_page(book_pk, page_number)
    return render(request, 'pdf_page.html', page)


class LeaveReview(LoginRequiredMixin, generic.View):
    login_url = 'user:login'
    template_name = 'add_review.html'

    def get(self, request, book_pk):
        form = ReviewForm()
        book = Book.objects.get(pk=book_pk)
        return render(request, self.template_name, {'form': form, 'book': book})

    def post(self, request, book_pk):
        form = ReviewForm(request.POST)
        book = Book.objects.get(pk=book_pk)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect('library:book', pk=book.pk)

        return render(request, self.template_name, {'form': form, 'book': book})
