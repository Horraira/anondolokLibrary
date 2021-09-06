from django.urls import path

from . import views

urlpatterns = [
    path('all_books_view', views.all_books_view, name='all-books-view'),
    path('historical_books', views.historical_books, name='historical_books'),
    path('user_appointment', views.user_appointment, name='user-appointment'),
    path('my_shelf', views.my_shelf, name='my-shelf'),
    path('book_info/<book_id>', views.book_info, name='/book-info'),
    path('renewal_info/<book_id>', views.renewal_info, name='/renewal-info'),
    path('renewal_confirmed/<book_id>',
         views.renewal_confirmed, name='/renewal-confirmed'),
    path('renewal_request', views.renewal_request, name='renewal-request'),
    path('search_books', views.search_books, name='search-books'),
    path('wished_books/<book_id>', views.wished_books, name='/wished-books'),

]
