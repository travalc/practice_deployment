from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^register$', views.register, name="register"),
    url(r'^login$', views.login, name="login"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^books$', views.books, name="books"),
    url(r'^add_book$', views.add_book, name="add_book"),
    url(r'^add_book_db$', views.add_book_db, name="add_book_db"),
    url(r'^books/(?P<id>\d+)$', views.book_page, name="book_page"),
    url(r'^add_review$', views.add_review, name="add_review"),
    url(r'^destroy_review$', views.destroy_review, name="destroy_review"),
    url(r'^users/(?P<id>\d+)$', views.user_page, name="user_page"),
]