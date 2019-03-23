from __future__ import unicode_literals
from django.db import models
import re


class UserManager(models.Manager):
    def basic_validator(self, postData):
        register_errors = {}
        if User.objects.filter(email = postData["email"]):
            register_errors['email'] = "Email is already being used. "
        if len(postData['email']) < 2:
            register_errors['email'] = "Email is not valid. "
        if len(postData['first_name']) < 2:
            register_errors['first_name'] = "First name must be at least two characters. "
        if len(postData['last_name']) < 2:
            register_errors['last_name'] = "Last name must be at least two characters. "
        if len(postData['password']) < 8:
            register_errors['password'] = "Password must be at least eight characters. "
        if len(postData['password']) != len(postData['confirmed_password']):
            register_errors['password'] = "Passwords must match. "
        if (not bool(re.match('^[a-zA-Z]+$', postData['first_name']))):
           register_errors["first_name"] = "First name should consist of only letters"
        if (not bool(re.match('^[a-zA-Z]+$', postData['last_name']))):
           register_errors["last_name"] = "Last name should consist of only letters"
        if (not bool(re.match(r'(\w+[.l\w])*@(\w+[.])*\w+', postData['email']))):
           register_errors["email"] = "Email is not a valid format"
        return register_errors
    def basic_validator_two(self, postData):
        user = User.objects.filter(email = postData["email"])
        login_errors = {}
        if not user:
            login_errors['email'] = "Email not found in database. "
        if user and not User.objects.filter(password = postData['password']):
            login_errors['password'] = "incorret password. "
        return login_errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField()
    password = models.CharField(max_length=45)
    birthdate = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()



class QuoteManager(models.Manager):
    def quote_validator(self, postData):
        quote_errors = {}
        if len(postData['author']) < 3:
            quote_errors['author'] = "Quoted by must be at least 4 characters. "
        if len(postData['quote']) < 9:
            quote_errors['quote'] = "Quote must be more than 10 characters. "
        return quote_errors


class Quote(models.Model):
    user = models.ForeignKey(User, related_name="user_quote")
    author = models.CharField(max_length= 100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()

class Favorite(models.Model):
    user = models.ForeignKey(User, related_name="user_favorite")
    author = models.CharField(max_length= 100)
    quote = models.ForeignKey(Quote, related_name="quote_favorite")
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
