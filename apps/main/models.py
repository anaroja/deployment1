# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt
import re 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def validate_reg(self, postData):
        errors = []
        name = postData['name']
        email = postData['email']
        username = postData['username']
        password = postData['password']
        confirm_password = postData['confirm_password']

        if len(name) is 0:
            errors.append('Name is required')
        elif len(name) < 2:
            errors.append('Name must be at least 2 characters')
        if len(username) is 0:
            errors.append('Username is required')
        elif len(username) < 4:
            errors.append('Username must be at least 4 characters')
        if len(email) is 0:
            errors.append('Email is required')
        elif not EMAIL_REGEX.match(email):
            errors.append('Email is invalid format')
        if len(password) is 0:
            errors.append('password is required')
        elif len(password) < 8:
            errors.append('password must be at least 8 characters')
        elif password != confirm_password:
            errors.append('passwords must match')
        
        if len(errors) > 0:
            # show errors to user
            return (False, errors)
        else:
            # first see if that email exists in users table
            result = self.filter(email=email)
            if len(result) > 0:
                # email exists
                errors.append('Email already exists')
                return (False, errors)
            else:
                # email doesn't exist and we can save
                new_user = self.create(
                    name = name,
                    username = username,
                    email = email,
                    password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                )
                return (True, new_user)
    
    def validate_log(self, postData):
        errors = []
        password = postData['password']
        email = postData['email']
        if len(password) is 0:
            errors.append('password is required')
        if len(email) is 0:
            errors.append('Email is required')
        elif not EMAIL_REGEX.match(email):
            errors.append('Email is invalid format')
        if len(errors) > 0:
            # show errors to user
            return (False, errors)
        else: 
            # find user by email
            results = self.filter(email=email)
            if len(results) > 0:
                # we found a user with that email
                user = results[0]
                if bcrypt.checkpw(password.encode(), user.password.encode()):
                    # successful password
                    return (True, user)
                #password fails
                else:
                    errors.append('Invalid Email/Password Combo')
                    return (False, errors)
            else:
                errors.append('Invalid Email/Password Combo')
                return (False, errors)

class QuoteManager(models.Manager):
    def quote_validator(self, postData):
        errors = []
        if len(postData['quoted_by']) is 0:
            errors.append('Quote is required')
        elif len(postData['quoted_by']) < 3:
            errors.append('Quote must be at least 3 characters')
        if len(postData['message']) is 0:
            errors.append('Message is required')
        elif len(postData['message']) < 10:
            errors.append('Message must be at least 10 characters')
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Quote(models.Model):
    message = models.TextField(default='')
    quoted_by = models.CharField(max_length=255)
    objects = QuoteManager()
    adders = models.ManyToManyField(User, related_name="added_quotes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name = "created_quotes")
