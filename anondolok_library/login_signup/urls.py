from django.urls import path

from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('landing', views.landing, name='landing'),
    path('ourBooks', views.ourBooks, name='our books'),
    path('unAuthSearch', views.unAuthSearch, name='Public Search'),
    path('admin-dashboard', views.admin_dashboard, name='admin dashboard'),
    # path('', views.user_dashboard, name='user dashboard'),
    path('user-dashboard', views.user_dashboard, name='user dashboard'),
    # path('home',views.home,name='home'),   #that will be a default page
    path('login/', views.login, name='login'),
    path('login/register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('edit_user_profile', views.edit_user_profile, name='edit_user_profile'),
    path('change_user_pass', views.change_user_pass, name='change_user_pass'),
    path('admin_pass_reset', views.admin_pass_reset, name='admin-pass-reset'),
    path('contact', views.contact, name='contact'),
    path('terms', views.terms, name='terms&conditions'),
    path('about', views.about, name='about-us'),
    path('verification_request/<user_id>',
         views.verification_request, name='/verification-request'),
    #path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]
