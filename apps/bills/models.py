from __future__ import unicode_literals

from django.db import models
from datetime import date
from dateutil.relativedelta import relativedelta
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
    def addBill(self, **kwargs):
        errors = []
        if len(kwargs['title']) == 0 or len(kwargs['date']) == 0 or len(kwargs['link']) == 0:
             errors.append('Please fill all the required fields')
        if kwargs['type'] == 'default' :
            errors.append('Please Select a Payment type')
        if kwargs['type'] == 'monthly':
            if len(kwargs['times']) == 0 and kwargs['undef_times'] == False:
                errors.append('Please tell us how many months do you need to pay this bill')
        if len(errors) is not 0:
            return (False, errors)
        else:
            if kwargs['type'] == 'monthly' and len(kwargs['times']) > 0:
                bill = Bill.objects.create(user_id=User.objects.get(id=kwargs['user_id']), title=kwargs['title'], amount=kwargs['amount'], date=kwargs['date'], payday=kwargs['payday'], link=kwargs['link'], times=kwargs['times'])
                bill.save()
            elif kwargs['type'] == 'monthly' and len(kwargs['times']) == 0:
                bill = Bill.objects.create(user_id=User.objects.get(id=kwargs['user_id']), title=kwargs['title'], amount=kwargs['amount'], date=kwargs['date'], payday=kwargs['payday'], link=kwargs['link'], times=kwargs['undef_times'])
                bill.save()
            else:
                bill = Bill.objects.create(user_id=User.objects.get(id=kwargs['user_id']), title=kwargs['title'], amount=kwargs['amount'], date=kwargs['date'], payday=kwargs['payday'], link=kwargs['link'], times= 1)
                bill.save()
            # bill.save()
            print bill," has been saved!"
            print "**********************"
            return (True, bill)

    def markBill(self, **kwargs):
        months = [29, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        # history_bill = History.objects.create(user_id=User.objects.get(id=kwargs['user_id']), bill_id=Bill.ojects.get(id=kwargs['bill_id']))
        # history_bill.save()
        bill = Bill.objects.get(id=kwargs['bill_id'])
        bill.times = bill.times - 1
        if bill.times > 0:
            bill.date = bill.date + relativedelta(months=+1)
            if bill.date.day < bill.payday and months[bill.date.month] >= bill.payday:
                print "time to change the payday!"
                difference = bill.payday - bill.date.day
                bill.date = bill.date + relativedelta(days =+ difference)
            bill.save()
        else:
            bill. delete()
        # deleting all records
        # bill = Bill.objects.all()
        # bill.delete()
        return (True, bill)



# class HistoryManager(models.Manager):


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
    link = models.CharField(max_length=200)
    date = models.DateTimeField()
    payday = models.IntegerField()
    times = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = BillManager()

class History(models.Model):
    user_id = models.ForeignKey(User)
    bill_id = models.ForeignKey(Bill)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = BillManager()
