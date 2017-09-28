# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse
from .models import *
from .forms import *

#helper function for form errors
def display_form_error(data, request):
    for field in data.errors:
        for message in data.errors[field]:
            string = field + ' field: ' + message
            messages.error(request, string)

# Create your views here.
def index(request):
    if 'user' in request.session:
        return redirect(reverse('belt_reviewer:books'))
    registration_form = Registration_Form()
    login_form = Login_Form()
    return render(request, 'index.html', {'registration_form': registration_form, 'login_form': login_form})

def register(request):
    form = Registration_Form(request.POST)
    if form.is_valid():
        data = User.objects.validate_registration(form.cleaned_data, request)
        if data == "Errors found":
            return redirect(reverse('belt_reviewer:index'))
        else:
            request.session['user'] = data
            return redirect(reverse('belt_reviewer:books'))
    else:
        display_form_error(form, request)
        return redirect(reverse('belt_reviewer:index'))

def login(request):
    form = Login_Form(request.POST)
    if form.is_valid():
        user = User.objects.validate_login(form.cleaned_data, request)
        if user == 'Errors found':
            return redirect(reverse('belt_reviewer:index'))
        else:
            request.session['user'] = user
            return redirect(reverse('belt_reviewer:books'))
    else:
        display_form_error(form, request)
        return redirect(reverse('belt_reviewer:index'))

def logout(request):
    #clear session and redirect to index when logout is clicked
    request.session.clear()
    return redirect(reverse('belt_reviewer:index'))

def books(request):
    data = order_home_page()
    return render(request, 'books.html', {'recent_three': data['recent_three'], 'rest': data['rest']})

def add_book(request):
    authors = [
        {
            'name':'-'
        },
    ]
    authors_query = Author.objects.all()
    for author in authors_query:
        authors.append(author)
    add_review_form = Add_Review_Form()
    add_book_form = Add_Book_Form()
    add_author_form = Add_Author_Form()
    return render(request, 'add_book.html', {'add_review_form': add_review_form, 'add_book_form': add_book_form, 'add_author_form': add_author_form, 'authors': authors})

def add_book_db(request):
    author_entry_validation = Author.objects.validate_author_entry(request.POST, request)
    if author_entry_validation != 'Success':
        return redirect(reverse('belt_reviewer:add_book'))
    else:
        add_book_form = Add_Book_Form(request.POST)
        add_review_form = Add_Review_Form(request.POST)
        add_author_form = Add_Author_Form(request.POST)
        if add_book_form.is_valid() and add_review_form.is_valid():
            if request.POST['choose_author'] != '-':
                author = request.POST['choose_author']
            else:
                if add_author_form.is_valid():
                    author = Author.objects.validate_new_author(add_author_form.cleaned_data, request)
                else:
                    display_form_error(add_author_form, request)
                    return redirect(reverse('belt_reviewer:add_book'))
            if author == "Errors Found":
                return redirect(reverse('belt_reviewer:add_book'))      
            book = Book.objects.validate_book(add_book_form.cleaned_data, request, request.session['user'], author)
            if book == "Errors Found":
                return redirect(reverse('belt_reviewer:add_book'))
            review = Review.objects.validate_review(add_review_form.cleaned_data, request, request.session['user'], book)
            if review is "Errors Found":
                return redirect(reverse('belt_reviewer:add_book'))
            book_query = Book.objects.get(title=book)
            book_id = book_query.id
            return redirect(reverse('belt_reviewer:book_page', kwargs = {'id': book_id}))               
        else:
            display_form_error(add_book_form, request)
            display_form_error(add_review_form, request)
            return redirect(reverse('belt_reviewer:add_book'))

def book_page(request, id):
    add_review_form = Add_Review_Form()
    book = get_book_data(request, id)
    return render(request, 'book.html', {'book': book, 'add_review_form': add_review_form})

def add_review(request):
    id = int(request.POST['book_id'])
    book = Book.objects.get(id=id)
    book_title = book.title
    review_form = Add_Review_Form(request.POST)
    if review_form.is_valid():
        review = Review.objects.validate_review(review_form.cleaned_data, request, request.session['user'], book_title)
    else:
        display_form_error(review_form, request)
    return redirect(reverse('belt_reviewer:book_page', kwargs = {'id': id}))

def destroy_review(request):
    id = int(request.POST['review_id'])
    book_id = int(request.POST['book_id'])
    review = Review.objects.get(id=id)
    review.delete()
    return redirect(reverse('belt_reviewer:book_page', kwargs = {'id': book_id}))

def user_page(request, id):
    data = get_user_data(id)
    return render(request, 'user.html', {'user': data})