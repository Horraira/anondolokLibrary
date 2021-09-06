from django.urls import path

from . import views

urlpatterns = [
    path('add_books', views.add_books, name='add books'),
    path('gen_qr', views.gen_qr, name='generate QR'),
    path('scan_book', views.scan_book, name='scan-book'),
    path('issue_books/<bookID>', views.issue_books, name='issue_books'),
    path('issue_book_info', views.issue_book_info, name='issue-book-info'),
    path('issue_book_list', views.issue_book_list, name='issue_book_list'),
    path('renewal_list', views.renewal_list, name='renewal-list'),
    path('appointment_list', views.appointment_list, name='appointment-list'),
    path('message_req', views.message_req, name='messages'),
    path('all_books', views.all_books, name='all-books'),
    path('member_management', views.member_management, name='member-management'),
    path('book_report', views.book_report, name='book-report'),
    path('edit_book/<book_id>', views.edit_book, name='/edit-book'),
    path('member_info/<member_id>', views.member_info, name='member-info'),
    path('book_detail/<book_id>', views.book_detail, name='/book-detail'),
    path('delete_book/<book_id>', views.delete_book, name='delete_book'),
    path('return_book/<book_id>', views.return_book, name='/return-book'),
    path('app_approve/<appointment_id>', views.app_approve, name='app-approve'),
    path('app_denied/<appointment_id>', views.app_denied, name='app-denied'),
    path('renewal_approve/<renewal_id>', views.renewal_approve, name='renewal-approve'),
    path('renewal_denied/<renewal_id>', views.renewal_denied, name='renewal-denied'),
    path('delete_user/<user_id>', views.delete_user, name='/delete-user'),
    path('verification_approved/<user_id>', views.verification_approved, name='/verification-approved'),
    path('verification_denied/<user_id>', views.verification_denied, name='/verification-denied'),
    path('cashPayment/<user_id>', views.cashPayment, name='/cash-payment'),
    path('bKashPayment/<user_id>', views.bKashPayment, name='/bKash-payment'),
]
