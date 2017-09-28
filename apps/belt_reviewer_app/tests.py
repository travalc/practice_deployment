# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.shortcuts import redirect, reverse
from .models import User, Book, Review, Author
from datetime import date

# Create your tests here.
# Model Tests
class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(first_name='Travis', last_name='Alcantara', email='travis.alcantara@gmail.com', password='testPassword', birthday=date.today())
    def test_user_fields(self):
        user = User.objects.get(email='travis.alcantara@gmail.com')
        self.assertEqual(user.first_name, 'Travis')
        self.assertEqual(user.last_name, 'Alcantara')
        self.assertEqual(user.email, 'travis.alcantara@gmail.com')
        self.assertEqual(user.password, 'testPassword')
        self.assertEqual(user.birthday, date.today())
class BookTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(first_name='Travis', last_name='Alcantara', email='travis.alcantara@gmail.com', password='testPassword', birthday=date.today())
        self.author = Author.objects.create(name='John Doe')
        Book.objects.create(title='testTitle', User=self.user, Author=self.author)
    def test_book_fields(self):
        book = Book.objects.get(title='testTitle')
        self.assertEqual(book.title, 'testTitle')
        self.assertEqual(book.User, self.user)
        self.assertEqual(book.Author, self.author)
class ReviewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(first_name='Travis', last_name='Alcantara', email='travis.alcantara@gmail.com', password='testPassword', birthday=date.today())
        self.author = Author.objects.create(name='John Doe')
        self.book = Book.objects.create(title='testTitle', User=self.user, Author=self.author)
        Review.objects.create(body='this is a test review', rating=5, User=self.user, Book=self.book)
    def test_review_fields(self):
        review = Review.objects.get(body='this is a test review')
        self.assertEqual(review.body, 'this is a test review')
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.User, self.user)
        self.assertEqual(review.Book, self.book)
class AuthorTestCase(TestCase):
    def setUp(self):
        Author.objects.create(name='John Doe')
    def test_author_fields(self):
        author = Author.objects.get(name='John Doe')
        self.assertEqual(author.name, 'John Doe')
# Model Manager Tests
class UserManagerTestCase(TestCase):
    def setUp(self):
        self.no_errors = User.objects.validate_user({
            'first_name': 'Travis',
            'last_name': 'Alcantara',
            'email': 'travalc@hotmail.com',
            'password': 'hellohello',
            'confirm_password': 'hellohello',
            'birthday': date.today()
        })
    def test_errors(self):
        self.assertEqual(len(self.no_errors), 0)
# Views Tests
class IndexTestCase(TestCase):
    def test_response(self):
        response = self.client.get(reverse('belt_reviewer:index'))
        #200 meaning get successful
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
class RegisterTestCase(TestCase):
    def test_response(self):
        response = self.client.get(reverse('belt_reviewer:register'))
        #302 meaning post route redirects
        self.assertEqual(response.status_code, 302)
class LoginTestCase(TestCase):
    def test_response(self):
        response = self.client.get(reverse('belt_reviewer:login'))
        self.assertEqual(response.status_code, 302)
class LogoutTestCase(TestCase):
    def test_response(self):
        response=self.client.get(reverse('belt_reviewer:logout'))
        self.assertEqual(response.status_code, 302)