from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q

from .methods.book_reader import view_single_page, progress_update, check_reviewed
from .models import Book
from .forms import ReviewForm


class BookDetail(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all()
        context['average_rating'] = self.object.reviews.aggregate(Avg('rating'))['rating__avg']
        if self.request.user.is_authenticated:
            context['reviewed'] = check_reviewed(self.request.user.pk, self.object.pk)
        return context


class BookList(generic.ListView):
    model = Book
    template_name = 'book_list.html'

    def get_queryset(self):
        search = self.request.GET.get('search')
        object_list = self.model.objects.all()
        if self.request.GET.get('search'):
            object_list = object_list.filter(Q(title__icontains=search) |
                                             Q(genres__genre__icontains=search) |
                                             Q(authors__name__icontains=search) |
                                             Q(authors__surname__icontains=search))
        return object_list.distinct()


@login_required(login_url='user:login')
def pdf_page_view(request, book_pk, page_number):
    page = view_single_page(book_pk, page_number)
    progress_update(request.user, book_pk, page_number, page['book_length'])
    return render(request, 'pdf_page.html', page)


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
