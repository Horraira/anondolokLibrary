from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime, timedelta
from .decorators import user_only
from .models import Appointments
from admin_panel.models import Books, IssueBook, wish_list, UserVerification
from django.db.utils import IntegrityError
# Create your views here.
# AbuFlexTuni%$^2021

# def verification(request):
#     user_id = request.user.id
#
#     checkUser = UserVerification.objects.get(user=user_id)
#     context = {'checkUser': checkUser}
#     return render(request, 'user_side_menu.html', context)


@user_only
def all_books_view(request):
    user_id = request.user.id
    checkUser = UserVerification.objects.get(user=user_id)

    book = Books.objects.all()
    return render(request, 'all_books_view.html', {'books': book, 'checkUser': checkUser})


@user_only
def story_books(request):
    user_id = request.user.id
    checkUser = UserVerification.objects.get(user=user_id)
    title = 'Historical and Traditional Books'

    book = Books.objects.filter(category__contains='History_&_Tradition')
    return render(request, 'categoryWiseBooks.html', {'books': book, 'checkUser': checkUser, 'title': title})


@user_only
def historical_books(request):
    user_id = request.user.id
    checkUser = UserVerification.objects.get(user=user_id)
    title = 'Historical and Traditional Books'

    book = Books.objects.filter(category__contains='History_&_Tradition')
    return render(request, 'categoryWiseBooks.html', {'books': book, 'checkUser': checkUser, 'title': title})


@user_only
def user_appointment(request):
    user_id = request.user.id
    user_name = request.user
    user = User.objects.get(pk=user_id)
    checkUser = UserVerification.objects.get(user=user_id)

    appointments = Appointments.objects.filter(user_name=user_name)

    if request.method == 'POST':
        req_date = request.POST['date']
        req_time = request.POST['time']

        appointment = Appointments(
            user=user, user_name=user_name, requested_date=req_date, requested_time=req_time)

        if appointment is not None:
            appointment.save()
            messages.info(request, 'Request sent successfully')
        else:
            messages.info(request, 'Request can not sent')

    return render(request, 'user_appointment.html', {'appointments': appointments, 'checkUser': checkUser})


@user_only
def book_info(request, book_id):
    user_id = request.user.id
    checkUser = UserVerification.objects.get(user=user_id)

    book = Books.objects.get(pk=book_id)
    return render(request, 'book_info.html', {'book': book, 'checkUser': checkUser})


@user_only
def my_shelf(request):
    user_id = request.user.id
    checkUser = UserVerification.objects.get(user=user_id)
    user = User.objects.get(pk=user_id)

    reading = IssueBook.objects.filter(user=user, is_return=False)
    read = IssueBook.objects.filter(user=user, is_return=True)
    wishList = wish_list.objects.filter(user=user, is_wished=True)

    context = {'reading': reading, 'read': read,
               'wishList': wishList, 'checkUser': checkUser}

    return render(request, 'shelf.html', context)


@user_only
def wished_books(request, book_id):
    user_id = request.user.id
    w_user = User.objects.get(pk=user_id)
    w_book = Books.objects.get(pk=book_id)

    wishList = wish_list(user=w_user, book=w_book, is_wished=True)
    # wishList.save()
    try:
        wishList.save()
    except IntegrityError as e:
        e = 'already added to wishlist'
        return redirect('/my_shelf', context={'e': e})

    return redirect('my-shelf')


@user_only
def renewal_request(request):
    user_id = request.user.id
    checkUser = UserVerification.objects.get(user=user_id)
    user = User.objects.get(pk=user_id)
    due_passed = IssueBook.objects.filter(
        user=user, due_date__lt=datetime.today(), is_return=False)
    items = IssueBook.objects.filter(user=user)

    context = {'due_passed': due_passed,
               'items': items, 'checkUser': checkUser}
    return render(request, 'renewal_request.html', context)


@user_only
def renewal_info(request, book_id):
    user_id = request.user.id
    checkUser = UserVerification.objects.get(user=user_id)
    book = Books.objects.get(pk=book_id)
    return render(request, 'renewal_info.html', {'book': book, 'checkUser': checkUser})


@user_only
def renewal_confirmed(request, book_id):
    user_id = request.user.id
    checkUser = UserVerification.objects.get(user=user_id)
    book = Books.objects.get(pk=book_id)

    status = IssueBook.objects.get(user=user_id, book=book_id, is_return=False)
    status.issue_status = 1
    status.save()
    return render(request, 'renewal_confirm.html', {'book': book, 'checkUser': checkUser})


@user_only
def search_books(request):
    user_id = request.user.id
    checkUser = UserVerification.objects.get(user=user_id)

    if request.method == 'POST':
        searched = request.POST['searched']
        books = Books.objects.filter(book_name__iexact=searched)
        category_books = Books.objects.filter(category__contains=searched)
        author_books = Books.objects.filter(author_name__iexact=searched)
        publisher_books = Books.objects.filter(publisher_name__iexact=searched)
        language_books = Books.objects.filter(language__iexact=searched)

    context = {
        'searched': searched,
        'books': books,
        'category_books': category_books,
        'checkUser': checkUser,
        'author_books': author_books,
        'publisher_books': publisher_books,
        'language_books': language_books,
    }

    return render(request, 'searched_books.html', context)


# -------------   live search ---------------------
@user_only
def main_view(request):
    pass


@user_only
def book_detail_view(request, book_id):
    pass
