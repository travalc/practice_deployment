# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import messages
import re
import bcrypt

#function to query database, organize data in order required for homepage
def order_home_page():
    reviews = Review.objects.all()
    ids = []
    full_list = []
    recent_three = []
    rest = []
    for review in reviews:
        ids.append(review.id)
    ids.sort()
    ids.reverse()
    for id in ids:
        review = Review.objects.get(id=id)
        user = User.objects.get(id=review.User_id)
        book = Book.objects.get(id=review.Book_id)
        full_list.append({
            'user': user,
            'review': review,
            'book': book
        })
    
    if len(full_list) >= 4:
        for item in full_list:
            exists = False
            for item2 in recent_three:
                if item2['book'].title == item['book'].title:
                    exists = True
            if exists == False:
                recent_three.append(item)
                if len(recent_three) < 3:
                    continue
                else:
                    break
            else:
                continue
                
        for item in full_list:
            #check if item exists in either recent three or rest list, if not then pusth to rest
            exists_in_recent_three = False
            exists_in_rest = False
            for item2 in recent_three:
                if item['book'].title == item2['book'].title:
                    exists_in_recent_three = True
            for item3 in rest:
                if item['book'].title == item3['book'].title:
                    exists_in_rest = True
            if exists_in_recent_three == False and exists_in_rest == False:
                rest.append(item)
    else:
        for item in full_list:
            exists_in_recent_three = False
            for item2 in recent_three:
                if item['book'].title == item2['book'].title:
                    exists_in_recent_three = True
            if exists_in_recent_three == False:
                recent_three.append(item)
    return {'recent_three': recent_three, 'rest': rest}

def get_user_data(id):
    user_query = User.objects.get(id=id)
    reviews_query = Review.objects.filter(User_id=id).values()
    books = []

    for review in reviews_query:
        book = Book.objects.get(id=review['Book_id'])
        exists = False
        for item in books:
            if item == book:
                exists = True
        if exists == False:
            books.append(book)
        else: 
            continue

    user = {
        'first_name': user_query.first_name,
        'last_name': user_query.last_name,
        'email': user_query.email,
        'review_count': len(reviews_query),
        'books': books
    }  

    return user

def get_book_data(request, id):
    user = User.objects.get(email=request.session['user']['email'])
    request.session['user']['id'] = user.id
    book_query = Book.objects.get(id=id)
    reviews = Review.objects.filter(Book_id=id)
    book = {
        'id': id,
        'title': book_query.title,
        'author': book_query.Author.name,
        'user': book_query.User,
        'reviews': []
    }
    for review in reviews.values():
        data = {
            'id': review['id'],
            'body': review['body'],
            'rating': review['rating'],
            'User_id': review['User_id'],
            'created_at': review['created_at']
        }
        book['reviews'].append(review)
    for review in book['reviews']:
        reviewed_by = User.objects.get(id=review['User_id'])
        review['reviewed_by'] = reviewed_by
    return book

# Model Managers
class UserManager(models.Manager):
    def validate_registration(self, data, request):
        errors = []
        name_regex = re.compile(r'^[A-Za-z]+$')
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        existing_email = User.objects.filter(email=data['email'])
        #check if first name and last name are at least 2 characters
        if len(data['first_name']) < 2 or len(data['last_name']) < 2:
            errors.append('First name and last name must both be at least 2 characters')
        #check if first name and last name are letters only
        if not name_regex.match(data['first_name']) or not name_regex.match(data['last_name']):
            errors.append('Both first and last name must be letters only!')
        #check if email is properly formatted utilizing regex
        if not email_regex.match(data['email']):
            errors.append('Email is improperly formatted')
        #check if a user in the database with the entered email already exists
        if len(existing_email) > 0:
            errors.append('A user with that email already exist')
        #check if password is at least 8 characters
        if len(data['password']) < 8:
            errors.append('Password must be at least 8 characters')
        #check if password and password confirmation match
        if data['password'] != data['confirm_password']:
            errors.append('Password and password confirmation must match')
        if len(errors) > 0:
            for error in errors:
                messages.error(request, error)
                return 'Errors found'
        else:
            first_name = data['first_name']
            last_name = data['last_name']
            email = data['email']
            password = data['password']
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            birthday = data['birthday']
            self.create(first_name=first_name, last_name=last_name, email=email, password=hashed_password, birthday=birthday)
            user = {
                'email': email,
                'first_name': first_name,
                'last_name': last_name
            }
            return user
    def validate_login(self, data, request):
        users = User.objects.filter(email = data['email'])
        if len(users) < 1:
            messages.error(request, 'No user with that email found')
            return 'Errors found'
        else:
            password = data['password']
            #check if password entered matches password in database
            if bcrypt.checkpw(password.encode(), users[0].password.encode()):
                user = {
                    'email': data['email'],
                    'first_name': users[0].first_name,
                    'last_name': users[0].last_name
                }
                return user
            else:
                messages.error(request, 'That password does not match what is on file')
                return 'Errors found'

class AuthorManager(models.Manager):
    def validate_author_entry(self, data, request):
        if data['new_author'] != '' and data['choose_author'] != '-':
            messages.error(request, 'Only one author allowed per book')
            return "Errors Found"
        elif data['new_author'] == '' and data['choose_author'] == '-':
            messages.error(request, 'Please choose an existing author or add a new one')
            return "Errors Found"
        else:
            return "Success"
    def validate_new_author(self, data, request):
        errors = []
        #Grab any existing authors
        existing_authors = Author.objects.filter(name=data['new_author'])
        #test if name field is not empty
        if len(data['new_author']) < 1:
            errors.append('Author name is required')
        if len(existing_authors) > 0:
            errors.append('Author already exists in our records')
        if len(errors) > 0:
            for error in errors:
                messages.error(request, error)
                return 'Errors Found'
        else:
            self.create(name=data['new_author'])
            return data['new_author']

class BookManager(models.Manager):
    def validate_book(self, data, request, user,  author):
        errors = []
        author_record = Author.objects.get(name=author)
        user_record = User.objects.get(email=user['email'])
        existing_book = Book.objects.filter(title=data['book_title'], Author=author_record)
        #test if title isn't empty
        if data['book_title'] == '':
            errors.append('Title is required')
        if len(existing_book) > 0:
            errors.append('A book with that author already exists in the database')
        if len(errors) > 0:
            for error in errors:
                messages.error(request, error)
                return 'Errors Found'
        else:
            self.create(title=data['book_title'], User=user_record, Author=author_record)
            return data['book_title']
        

class ReviewManager(models.Manager):
    def validate_review(self, data, request, user, book):
        errors = []
        book_record = Book.objects.get(title=book)
        user_record = User.objects.get(email=user['email'])
        #test if body isn't empty
        if len(data['body']) < 1:
            errors.append('Review body is required')
        if data['rating'] == '-':
            errors.append('Please choose a valid rating')
        if len(errors) > 0:
            for error in errors:
                messages.error(request, error)
                return 'Errors Found'
        else:
            self.create(body=data['body'], rating=data['rating'], User=user_record, Book=book_record)
            return book
# Models
class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    birthday = models.DateField(auto_now=False, auto_now_add=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()

class Author(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = AuthorManager()

class Book(models.Model):
    title = models.CharField(max_length=100)
    User = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    Author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = BookManager()
    
class Review(models.Model):
    body = models.TextField()
    rating = models.IntegerField(default=0)
    User = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    Book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = ReviewManager()