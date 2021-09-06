from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
import qrcode
from datetime import datetime, timedelta
import qrcode.image.svg
from io import BytesIO
from .models import Books, IssueBook, UserVerification
from login_signup.models import Contact
from django.db.models import Q
from user_panel.models import Appointments

from .decorators import allowed_users, admin_only
from django.utils.datastructures import MultiValueDictKeyError


# Create your views here.
# AbuFlexTuni%$^2021

@admin_only
@allowed_users(allowed_roles=['ADMIN'])
def add_books(request):
    if request.method == 'POST':
        book_name = request.POST['book_name']
        author_name = request.POST['author_name']
        category = request.POST['category']
        book_pages = request.POST['pages']
        # quantity = request.POST['quantity']
        language = request.POST['language']
        price = request.POST['price']
        isbn_number = request.POST['isbn_number']
        doi_number = request.POST['doi_number']
        accession_number = request.POST['accession_number']
        publisher_name = request.POST['publisher_name']
        publisher_date = request.POST['publisher_date']
        shelf_number = request.POST['shelf_number']
        description = request.POST['description']
        try:
            cover_photo = request.FILES['cover_photo']
        except MultiValueDictKeyError as e:
            e = 'You have to upload the Cover Photo'
            return render(request, "add_books.html", context={'e': e})

        book = Books(book_name=book_name, author_name=author_name, category=category, book_pages=book_pages, language=language,
                     price=price, isbn_number=isbn_number, doi_number=doi_number, accession_number=accession_number,
                     publisher_name=publisher_name, publisher_date=publisher_date, shelf_number=shelf_number,
                     description=description, cover_photo=cover_photo)

        if book is not None:
            book.save()
            return redirect('generate QR')
        else:
            messages.info(request, 'Partial data is not excepted')
            return redirect('add books')

    return render(request, 'add_books.html')


@admin_only
@allowed_users(allowed_roles=['ADMIN'])
def gen_qr(request):
    context = {}

    fletch = Books.objects.all().last()
    book_id = fletch.id

    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(book_id, image_factory=factory, box_size=20)
    stream = BytesIO()
    img.save(stream)
    context['svg'] = stream.getvalue().decode()

    return render(request, 'gen_qr.html', context=context)


@admin_only
@allowed_users(allowed_roles=['ADMIN'])
def message_req(request):
    message = Contact.objects.all()

    return render(request, 'messages.html', {'messages': message})


@admin_only
@allowed_users(allowed_roles=['ADMIN'])
def all_books(request):
    book = Books.objects.all()

    return render(request, 'all_books_table.html', {'books': book})


@admin_only
@allowed_users(allowed_roles=['ADMIN'])
def edit_book(request, book_id):
    book = Books.objects.get(pk=book_id)

    if request.method == 'POST':
        book.book_name = request.POST['book_name']
        book.author_name = request.POST['author_name']
        book.category = request.POST['category']
        book.book_pages = request.POST['pages']
        book.price = request.POST['price']
        # quantity = request.POST['quantity']
        book.language = request.POST['language']
        book.isbn_number = request.POST['isbn_number']
        book.doi_number = request.POST['doi_number']
        book.accession_number = request.POST['accession_number']
        book.publisher_name = request.POST['publisher_name']
        book.publisher_date = request.POST['publisher_date']
        book.shelf_number = request.POST['shelf_number']
        book.description = request.POST['description']
        book.save()

        return redirect('all-books')

    return render(request, 'edit_book.html', {'book': book})


@admin_only
@allowed_users(allowed_roles=['ADMIN'])
def issue_books(request, bookID):
    if request.method == 'POST':
        # user = request.POST['user_id']
        user = request.POST['username']
        # book = request.POST['book_id']
        borrower = User.objects.get(username=user)
        lending_book = Books.objects.get(pk=bookID)
        # issue_book = IssueBook.objects.get(book=book)
        # due_date = datetime.now().date() + timedelta(days=7)
        due_date = request.POST['due_date']

        landing = IssueBook(due_date=due_date, is_return=False, user=borrower, book=lending_book)

        # if issue_book.is_return:
        if landing is not None:
            try:
                landing.save()
                return redirect('issue-book-info')
            except IntegrityError as e:
                e = 'This book is already borrowed by this user'
                return render(request, "issue_books.html", context={'e': e})
        else:
            messages.info(request, 'This book is not returned')
            return redirect('issue_books')

    return render(request, 'issue_books.html')


@admin_only
@allowed_users(allowed_roles=['ADMIN'])
def issue_book_info(request):
    issued_book = IssueBook.objects.all().last()

    book_id = issued_book.book_id
    book = Books.objects.get(pk=book_id)

    context = {'book': book,
               'due_date': issued_book.due_date,
               'issue_date': issued_book.issue_date,
               'user_id': issued_book.user_id
               }

    return render(request, 'issued_info.html', context)


@admin_only
@allowed_users(allowed_roles=['ADMIN'])
def issue_book_list(request):
    issued_book = IssueBook.objects.filter(is_return=False)

    return render(request, 'issue_book_list.html', {'issuedBook': issued_book})


@admin_only
@allowed_users(allowed_roles=['ADMIN'])
def scan_book(request):
    book_id = request.POST['book_id']
    issue_book = IssueBook.objects.filter(book=book_id).last()
    try:
        if issue_book is not None:
            if issue_book.is_return:
                try:
                    book_info = Books.objects.get(pk=book_id)
                    due_date = datetime.now().date() + timedelta(days=15)
                    context = {'book': book_info, 'due_date': due_date}
                    return render(request, 'issue_books.html', context)
                except Books.DoesNotExist:
                    e = 'This book does not exist'
                    return render(request, "admin_dashboard.html", context={'e': e})
            else:
                book_info = Books.objects.get(pk=book_id)
                return render(request, "book_return.html", {'book': book_info})
        else:
            try:
                book_info = Books.objects.get(pk=book_id)
                due_date = datetime.now().date() + timedelta(days=15)
                context = {'book': book_info, 'due_date': due_date}
                return render(request, 'issue_books.html', context)
            except Books.DoesNotExist:
                e = 'This book does not exist'
                return render(request, "admin_dashboard.html", context={'e': e})
    except IssueBook.DoesNotExist:
        book_info = Books.objects.get(pk=book_id)
        due_date = datetime.now().date() + timedelta(days=15)
        context = {'book': book_info, 'due_date': due_date}
        return render(request, 'issue_books.html', context)

    # return render(request, 'issue_books.html')


@admin_only
@allowed_users(allowed_roles=['ADMIN'])
def delete_book(request, book_id):
    book = Books.objects.get(pk=book_id)
    book.cover_photo.delete(save=True)
    # book.cover_photo.storage.delete()
    book.delete()
    return redirect('all-books')


@admin_only
@allowed_users(allowed_roles=['ADMIN'])
def book_report(request):
    total_book = Books.objects.count()
    issued_book = IssueBook.objects.count()
    returned_book = IssueBook.objects.filter(is_return=False).count()

    context = {'total_book': total_book, 'issued_book': issued_book, 'returned_book': returned_book}
    return render(request, 'reports.html', context)


@admin_only
@allowed_users(allowed_roles=['ADMIN'])
def appointment_list(request):
    appointment = Appointments.objects.all()
    return render(request, 'appointment_list.html', {'appointment': appointment})


@admin_only
@allowed_users(allowed_roles=['ADMIN'])
def app_approve(request, appointment_id):
    appointment = Appointments.objects.get(pk=appointment_id)
    appointment.check_approve = 1
    appointment.save()
    return redirect('appointment-list')


@admin_only
@allowed_users(allowed_roles=['ADMIN'])
def app_denied(request, appointment_id):
    appointment = Appointments.objects.get(pk=appointment_id)
    appointment.check_approve = 0
    appointment.save()
    return redirect('appointment-list')


# @admin_only
# @allowed_users(allowed_roles=['ADMIN'])
# def member_management(request):
#     user = User.objects.filter(is_superuser=False)
#     return render(request, 'members_list.html', {'context': user})
@admin_only
@allowed_users(allowed_roles=['ADMIN'])
def member_management(request):
    user = UserVerification.objects.all()
    return render(request, 'members_list.html', {'context': user})


@admin_only
@allowed_users(allowed_roles=['ADMIN'])
def member_info(request, member_id):
    member = User.objects.get(pk=member_id)
    userInfo = UserVerification.objects.get(user_id=member)
    print(userInfo)
    return render(request, 'member_info.html', {'user': member, 'userInfo': userInfo})


@admin_only
@allowed_users(allowed_roles=['ADMIN'])
def verification_approved(request, user_id):
    user = UserVerification.objects.get(user=user_id)
    user.verification_status = 1
    user.is_verified = True
    user.save()
    return redirect('member-management')


@admin_only
@allowed_users(allowed_roles=['ADMIN'])
def verification_denied(request, user_id):
    user = UserVerification.objects.get(user=user_id)
    user.verification_status = 3
    user.save()
    return redirect('member-management')


@admin_only
@allowed_users(allowed_roles=['ADMIN'])
def cashPayment(request, user_id):
    user = UserVerification.objects.get(user=user_id)
    user.payment = 'cash'
    user.verification_status = 1
    user.is_verified = True
    user.save()
    return redirect('member-management')


@admin_only
@allowed_users(allowed_roles=['ADMIN'])
def bKashPayment(request, user_id):
    if request.method == 'POST':
        user = UserVerification.objects.get(user=user_id)
        user.payment = request.POST.get('TrxID')
        user.verification_status = 1
        user.is_verified = True
        user.save()
    return redirect('member-management')


@admin_only
@allowed_users(allowed_roles=['ADMIN'])
def renewal_list(request):
    renewal = IssueBook.objects.filter(~Q(issue_status=0), is_return=False)
    return render(request, 'renewal_list.html', {'renewal': renewal})


@admin_only
@allowed_users(allowed_roles=['ADMIN'])
def renewal_approve(request, renewal_id):
    renewal = IssueBook.objects.get(pk=renewal_id)
    renewal.due_date = datetime.now().date() + timedelta(days=15)
    renewal.issue_status = 2
    renewal.save()
    return redirect('renewal-list')


@admin_only
@allowed_users(allowed_roles=['ADMIN'])
def renewal_denied(request, renewal_id):
    renewal = IssueBook.objects.get(pk=renewal_id)
    renewal.issue_status = 3
    renewal.save()
    return redirect('renewal-list')


@admin_only
@allowed_users(allowed_roles=['ADMIN'])
def delete_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.delete()
    return redirect('member-management')


@admin_only
def book_detail(request, book_id):
    book = Books.objects.get(pk=book_id)
    return render(request, 'book_details.html', {'book': book})


@admin_only
@allowed_users(allowed_roles=['ADMIN'])
def return_book(request, book_id):
    book = IssueBook.objects.filter(book=book_id).last()
    book.is_return = True
    book.issue_status = 0
    book.save()
    return redirect('admin dashboard')
