from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required

from .methods.book_reader import view_single_page
from .models import Book


class BookDetail(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'


class BookList(generic.ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'book'


@login_required(login_url='user:login')
def pdf_page_view(request, book_pk, page_number):
    page = view_single_page(book_pk, page_number)
    return render(request, 'pdf_page.html', page)


def search(request):
    query_text = request.GET['search_text']
    query_result = Book.objects.filter(title__icontains=query_text)
    data = {'query_text_c': query_text,
            'query_result_c': query_result}

    return render(request, "search.html", context=data)
