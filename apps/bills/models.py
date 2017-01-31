from __future__ import unicode_literals

from django.db import models

import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
PHONE_REGEX = re.compile(r'^\+?1?\d{9,15}$')


class UserManager(models.Manager):
    def register(self, **kwargs):
        errors = []
        if len(kwargs['first_name']) < 3:
             errors.append('First name is not longer than 2 letters.')
        if not NAME_REGEX.match(kwargs['first_name']):
            errors.append('First name must be letters.')
        if len(kwargs['last_name']) < 3:
            errors.append('Last name is not longer than 2 letter.')
        if not NAME_REGEX.match(kwargs['last_name']):
            errors.append('Last name must be letters.')
        if len(kwargs['email']) == 0:
            errors.append('Invalid Email length.')
        if not EMAIL_REGEX.match(kwargs['email']):
            errors.append('Invalid email.')
        if User.objects.filter(email=kwargs["email"]):
            errors.append("Email already exists!")
        if not PHONE_REGEX.match(kwargs['phone_number']):
            errors.append('Enter valid phone number.')
        if len(kwargs['password']) < 8:
            errors.append('Password must be longer than 8 characters.')
        if kwargs['password'] != kwargs['confirm_pw']:
            errors.append('Password does not match.')
        if len(errors) is not 0:
            return (False, errors)
        else:
            hashed = bcrypt.hashpw((kwargs['password']).encode(), bcrypt.gensalt())
            info = User.objects.create(first_name=kwargs['first_name'], last_name=kwargs['last_name'], phone_number=kwargs['phone_number'], email=kwargs['email'], password=hashed)
            info.save()
            print info
            return (True, info)

    def login(self, **kwargs):
        try:
            user = User.objects.get(email=kwargs['email'])
        except:
            return (False, "Login fields are invalid.")

        if User.objects.get(email=kwargs['email']):
            hashed = bcrypt.hashpw((kwargs['password']).encode(), User.objects.get(email=kwargs['email']).password.encode())
            if User.objects.get(email=kwargs['email']).password == hashed:
                info = User.objects.get(email=kwargs['email'])
                return (True, info)
            else:
                return (False, 'Password does not match.')
        else:
            return (False, 'Email does not exist.')

class BillManager(models.Manager):
    print 'Hello'

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Bill(models.Model):
    user_id = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    amount = models.FloatField(null=True)
    date = models.DateTimeField()
    reccurrence = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = BillManager()
