import PyPDF2
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

import base64
from datetime import datetime
from library.models import Book, ReadingProgress, Review


def view_single_page(book_pk: int, page: int) -> dict:
    book = get_object_or_404(Book, pk=book_pk)
    with open(book.pdf.name, 'rb') as file:
        data = PyPDF2.PdfReader(file).pages[page-1]
        display_page = PyPDF2.PdfWriter()
        display_page.add_page(data)
        response = HttpResponse(content_type='application/pdf')
        display_page.write(response)
        pdf_data = f"data:application/pdf;base64,\
        {base64.b64encode(response.content).decode('utf-8')}#toolbar=0"
        context = {
            'book': book,
            'page_pdf': pdf_data,
            'page_number': page,
            'prev_page': page-1,
            'next_page': page+1,
            'book_length': len(PyPDF2.PdfReader(file).pages)
        }
        return context


def progress_update(user, book_pk, page, length):
    progress, created = ReadingProgress.objects.get_or_create(user=user, book_id=book_pk)
    if page == length:
        progress.finished = datetime.now()
    if progress.last_page < page <= length:
        progress.last_page = page
    else:
        pass
    progress.save()


def check_reviewed(user, book_pk):
    try:
        review = bool(Review.objects.get(user=user, book=book_pk))
    except Review.DoesNotExist:
        review = False
    return review
