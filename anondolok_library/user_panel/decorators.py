from django.http import HttpResponse
from django.shortcuts import render, redirect


def user_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'ADMIN':
            return redirect('admin dashboard')

        if group == 'USERS':
            return view_func(request, *args, **kwargs)

    return wrapper_function