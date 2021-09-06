from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import auth, User
from django.shortcuts import render, redirect
from .decorators import unauthenticated_user, allowed_users, user_only, admin_only
from .forms import CreateUserForm
from .models import Contact
from admin_panel.models import Books, IssueBook, UserVerification

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

UserModel = get_user_model()
# from .models import user
# AbuFlexTuni%$^2021
# sohanAbuFlexTuni%$^2021

# Create your views here.


def landing(request):
    return render(request, 'landing.html')


def ourBooks(request):
    books = Books.objects.all()
    return render(request, 'ourBooks.html', {'books': books})


def unAuthSearch(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        books = Books.objects.filter(book_name__iexact=searched)
        category_books = Books.objects.filter(category__contains=searched)
        author_books = Books.objects.filter(author_name__iexact=searched)
        publisher_books = Books.objects.filter(publisher_name__iexact=searched)
        language_books = Books.objects.filter(language__iexact=searched)

    context = {
        'books': books,
        'category_books': category_books,
        'author_books': author_books,
        'publisher_books': publisher_books,
        'language_books': language_books,
    }

    return render(request, 'unAuthSearch.html', context)
    # else:
    #     books = Books.objects.all()
    #     return render(request, 'ourBooks.html', {'books': books})


@allowed_users(allowed_roles=['ADMIN'])
@admin_only
def admin_dashboard(request):
    total_book = Books.objects.count()
    issued_book = IssueBook.objects.count()
    returned_book = IssueBook.objects.filter(is_return=False).count()

    context = {'total_book': total_book,
               'issued_book': issued_book, 'returned_book': returned_book}
    return render(request, 'admin_dashboard.html', context)


@login_required(login_url='landing')  # only logged in user can view this page
@user_only
def user_dashboard(request):
    user_id = request.user.id

    # issued books and returned books amount
    issued = IssueBook.objects.filter(user=user_id, is_return=False).count()
    returned = IssueBook.objects.filter(user=user_id, is_return=True).count()
    checkUser = UserVerification.objects.get(user=user_id)

    # favourite genre
    fiction = IssueBook.objects.filter(
        user=user_id, book__category__contains='Fiction').count()
    novel = IssueBook.objects.filter(
        user=user_id, book__category__contains='Novel').count()
    historical = IssueBook.objects.filter(
        user=user_id, book__category__contains='Historical').count()
    thriller = IssueBook.objects.filter(
        user=user_id, book__category__contains='Thriller').count()
    science_fiction = IssueBook.objects.filter(
        user=user_id, book__category__contains='Science Fiction').count()
    mystery = IssueBook.objects.filter(
        user=user_id, book__category__contains='Mystery').count()
    poetry = IssueBook.objects.filter(
        user=user_id, book__category__contains='Poetry').count()
    horror = IssueBook.objects.filter(
        user=user_id, book__category__contains='Horror').count()
    humour = IssueBook.objects.filter(
        user=user_id, book__category__contains='Humour').count()
    crime = IssueBook.objects.filter(
        user=user_id, book__category__contains='Crime').count()
    politics = IssueBook.objects.filter(
        user=user_id, book__category__contains='Politics').count()
    motivational = IssueBook.objects.filter(
        user=user_id, book__category__contains='Motivational').count()
    biography = IssueBook.objects.filter(
        user=user_id, book__category__contains='Biography').count()

    book_dic = {
        fiction: "fiction",
        novel: "Novel",
        historical: "historical",
        thriller: "thriller",
        science_fiction: "science fiction",
        mystery: "mystery",
        poetry: "poetry",
        horror: "horror",
        humour: "humor",
        crime: "crime",
        politics: "politics",
        motivational: "motivational",
        biography: "biography"
    }
    books = [fiction, novel, historical, thriller, science_fiction, mystery,
             poetry, horror, humour, crime, politics, motivational, biography]
    books.sort()

    first_amount = books[-1]
    second_amount = books[-2]
    third_amount = books[-3]

    first_book = book_dic.get(books[-1])
    second_book = book_dic.get(books[-2])
    third_book = book_dic.get(books[-3])

    context = {
        'issued_book': issued,
        'returned_book': returned,
        'first_amount': first_amount,
        'first_book': first_book,
        'second_amount': second_amount,
        'second_book': second_book,
        'third_amount': third_amount,
        'third_book': third_book,
        'checkUser': checkUser
    }

    return render(request, 'user_dashboard.html', context)


@unauthenticated_user  # logged in user can't visit the page
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        reg_user = auth.authenticate(username=username, password=password)

        if reg_user is not None:
            auth.login(request, reg_user)
            return redirect(user_dashboard)
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, "signin.html")


@unauthenticated_user  # logged in user can't visit the page
def register(request):
    form = CreateUserForm()  # create a form to sent template as context

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        occupation = request.POST["occupation"]
        dateOfBirth = request.POST["dateOfBirth"]
        presentAddress = request.POST["presentAddress"]

        if form.is_valid():
            user = form.save()
            user.save()
            verification = UserVerification(user=user, is_verified=False, presentAddress=presentAddress,
                                            dateOfBirth=dateOfBirth, occupation=occupation)
            verification.save()
            # get the username from form & cleaned data used to get only
            username = form.cleaned_data.get('username')
            # the username

            group = Group.objects.get(name='USERS')
            user.groups.add(group)

            messages.success(request, 'Account is created for ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'signup.html', context)

# --------------- Email confirmation for user registration section ---------------
# @unauthenticated_user  # logged in user can't visit the page
# def register(request):
#     form = CreateUserForm()  # create a form to sent template as context

#     if request.method == 'POST':
#         form = CreateUserForm(request.POST)
#         occupation = request.POST["occupation"]
#         dateOfBirth = request.POST["dateOfBirth"]
#         presentAddress = request.POST["presentAddress"]
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             verification = UserVerification(user=user, is_verified=False, presentAddress=presentAddress,
#                                             dateOfBirth=dateOfBirth, occupation=occupation)
#             verification.save()
#             # get the username from form & cleaned data used to get only
#             username = form.cleaned_data.get('username')
#             # the username

#             group = Group.objects.get(name='USERS')
#             user.groups.add(group)

#             current_site = get_current_site(request)
#             mail_subject = 'Activate your account.'
#             message = render_to_string('acc_active_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': default_token_generator.make_token(user),
#             })
#             to_email = form.cleaned_data.get('email')
#             email = EmailMessage(
#                 mail_subject, message, to=[to_email]
#             )
#             email.send()
#             return HttpResponse('A confirmation link will sent to your email.\n'
#                                 'Please login your mail and click the link to complete the registration.\n'
#                                 'You may need to check the spam messages.')

#     context = {'form': form}
#     return render(request, 'signup.html', context)


# def activate(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = UserModel._default_manager.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         messages.success(request, 'Account is activated for ' + user.username)
#         return redirect('login')
#         # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
#     else:
#         return HttpResponse('Activation link is invalid!')


@user_only
def edit_user_profile(request):
    pid = request.user.id
    checkUser = UserVerification.objects.get(user=pid)
    context = {'checkUser': checkUser}

    if request.method == 'POST':
        user = User.objects.get(pk=pid)
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('phone')
        user.save()

        userInfo = UserVerification.objects.get(user_id=user)
        userInfo.presentAddress = request.POST.get('address')
        userInfo.profilePic = request.FILES.get('profilePic')

        userInfo.save()

        messages.success(request, 'Profile updated.')
        return redirect('edit_user_profile')

    return render(request, 'user_settings.html', context)


@user_only
def verification_request(request, user_id):
    user = UserVerification.objects.get(user=user_id)
    user.verification_status = 2
    user.save()
    return redirect('edit_user_profile')


@user_only
def change_user_pass(request):
    pid = request.user.id
    checkUser = UserVerification.objects.get(user=pid)
    context = {'checkUser': checkUser}

    if request.method == 'POST':
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            user = User.objects.get(pk=pid)
            user.set_password(password)
            user.save()

            messages.success(request, 'Password updated.')
            return redirect('login')
        else:
            messages.success(request, 'Password not match.')

    return render(request, 'user_settings.html', context)


@allowed_users(allowed_roles=['ADMIN'])
def admin_pass_reset(request):
    pid = request.user.id

    if request.method == 'POST':
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            user = User.objects.get(pk=pid)
            user.set_password(password)
            user.save()

            messages.success(request, 'Password updated.')
            return redirect('login')
        else:
            messages.success(request, 'Password not match.')

    return render(request, 'admin_setting.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


def contact(request):
    if request.method == 'POST':
        name = request.POST['c_name']
        mail = request.POST['c_mail']
        phone = request.POST['phone']
        message = request.POST['message']

        contact_form = Contact(c_name=name, c_mail=mail,
                               c_phone=phone, c_message=message)

        if contact_form is not None:
            contact_form.save()
            return redirect('landing')
        else:
            messages.info(request, 'Message can not be delivered')
            return redirect('contact')

    return render(request, 'contact.html')


def terms(request):
    return render(request, 'term&conditions.html')


def about(request):
    return render(request, 'about.html')
