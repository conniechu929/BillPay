from __future__ import unicode_literals
from django.forms import ModelForm
from django.db import models
from django.core.exceptions import ValidationError

import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
PHONE_REGEX = re.compile(r'^\+?1?\d{9,15}$')

def validateLengthGreaterThanTwo(value):
    if len(value)< 3:
        raise ValidationError(
          '{} must be longer than: 2'.format(value)
        )

def validName(value):
    if not NAME_REGEX.match(value):
        raise ValidationError(
            '{} must be letters'.format(value)
        )

def validEmail(value):
    if not EMAIL_REGEX.match(value):
        raise ValidationError(
            '{} not a valid email.'.format(value)
        )

def emailcheck(value, **kwargs):
    return value

def phonecheck(value):
    if not PHONE_REGEX.match(value):
        raise ValidationError(
            'Enter valid phone number.'
        )

def passLength(value):
    if len(value) < 8:
        raise ValidationError(
            'Password must be longer than 8 characters.'
        )


class User(models.Model):
    first_name = models.CharField(max_length=45, validators = [validateLengthGreaterThanTwo, validName])
    last_name = models.CharField(max_length=45, validators = [validateLengthGreaterThanTwo, validName])
    email = models.EmailField(max_length=45, blank=True, null= True, unique= True, validators = [validateLengthGreaterThanTwo, validEmail, emailcheck])
    phone_number = models.CharField(max_length=15, validators = [phonecheck])
    password = models.CharField(max_length=255, validators = [passLength])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Bill(models.Model):
    user_id = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    amount = models.FloatField(null=True)
    date = models.DateTimeField()
    reccurrence = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
