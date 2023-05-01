from django.shortcuts import render, redirect, reverse
from .forms import RegistrationForm, RatingReviewForm
from django.contrib.auth import login
from django.contrib import messages
from django.views import generic
from .models import RatingReview
from django.contrib.auth.decorators import login_required

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


# class ReviewList(generic.ListView):
#     model = RatingReview
#     paginate_by = 3
#     context_object_name = "reviewss"
#     template_name = "review_list.html"
#
#     def get_queryset(self):
#         query = RatingReview.objects.filter(review=self.request.book).order_by("date")
#         return query


class LeaveRatingReview(generic.edit.FormMixin, generic.DetailView):
    model = RatingReview
    form_class = RatingReviewForm
    template_name = '/book_detail.html'
    context_object_name = 'leave_review'

    # after submitting the form:
    def get_success_url(self):
        return reverse('leave_review_n', kwargs={'pk': self.object.id})

    # post, we use from form_valid below
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.book = self.object
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)



# def leave_review(request, book_id):
#     url = request.META.get('HTTP_REFERER')
#     if request.method == 'POST':
#         try:
#             reviews = RatingReview.objects.get(user__id=request.user.id, book__id=book_id)
#             form = RatingReviewForm(request.POST, instance=reviews)
#             form.save()
#             messages.success(request, 'Your Review has been updated.')
#             return redirect(url)
#         except RatingReview.DoesNotExist:
#             form = RatingReviewForm(request.POST)
#             if form.is_valid():
#                 data = RatingReview()
#                 data.subject = form.cleaned_data['subject']
#                 data.rating = form.cleaned_data['rating']
#                 data.review = form.cleaned_data['review']
#                 data.ip = request.META.get('REMOTE_ADDR')
#                 data.book_id = book_id
#                 data.user_id = request.user.id
#                 data.save()
#                 messages.success(request, 'Your Review has been submitted.')
#                 return redirect(url)
