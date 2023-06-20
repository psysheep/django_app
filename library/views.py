from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q

from .methods.helper import encode_single_page, update_progress, check_reviewed, get_user_page
from .models import Book
from user.models import Bookmarks


class BookDetail(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all()
        context['average_rating'] = self.object.reviews.aggregate(Avg('rating'))['rating__avg']

        if self.request.user.is_authenticated:
            context['reviewed'] = check_reviewed(self.request.user.pk, self.object.pk)
            context['page'] = get_user_page(self.request.user.pk, self.object.pk)

        return context


class BookList(generic.ListView):
    model = Book
    template_name = 'book_list.html'

    def get_queryset(self):
        search = self.request.GET.get('search')
        object_list = self.model.objects.all()

        if self.request.GET.get('search'):
            object_list = object_list.filter(
                Q(title__contains=search) |
                Q(genres__genre__contains=search) |
                Q(authors__name__contains=search) |
                Q(authors__surname__contains=search)
            )
        return object_list.distinct()


@login_required(login_url='user:login')
def page_view(request, book_pk, page_number):
    page = encode_single_page(book_pk, page_number)
    update_progress(request.user, book_pk, page_number, page['book_length'])

    if request.method == 'POST':
        if 'bookmark_title' in request.POST:
            title = request.POST['bookmark_title']
            bookmark = Bookmarks(user=request.user, book_id=book_pk, page=page_number, header=title)
            bookmark.save()

        if 'goto' in request.POST:
            return redirect('library:page_view', book_pk=book_pk, page_number=request.POST['goto'])

    return render(request, 'book_page.html', page)
