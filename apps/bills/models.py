from __future__ import unicode_literals
from django.forms import ModelForm
from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

from dateutil.relativedelta import relativedelta

import bcrypt
import re
# import arrow

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
            # schedule_reminder(bill)
            print bill," has been saved!"
            print "**********************"
            return (True, bill)

    def updateBill(self, **kwargs):
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
            bill = Bill.objects.get(id=kwargs['id'])
            bill.title = kwargs['title']
            bill.amount=kwargs['amount']
            bill.date=kwargs['date']
            bill.payday=kwargs['payday']
            bill.link=kwargs['link']
            if kwargs['type'] == 'monthly' and len(kwargs['times']) > 0:
                bill.times=kwargs['times']
            elif kwargs['type'] == 'monthly' and len(kwargs['times']) == 0:
                bill.times=kwargs['undef_times']
            else:
                bill.times= 1
            bill.save()
            print bill," has been updated!"
            print "**********************"
            return (True, bill)

    def markBill(self, **kwargs):
        months = [29, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        bill = Bill.objects.get(id=kwargs['bill_id'])
        history_bill = History.objects.create(user_id=User.objects.get(id=kwargs['user_id']), title=bill.title, amount=bill.amount, link=bill.link)
        history_bill.save()
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
        # bill = History.objects.all()
        # bill.delete()
        return (True, bill)




# class HistoryManager(models.Manager):


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
    link = models.CharField(max_length=200)
    date = models.DateTimeField()
    payday = models.IntegerField()
    times = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = BillManager()

    def schedule_reminder(self):
        """Schedules a Celery task to send a reminder about this appointment"""

        # Calculate the correct time to send this reminder
        appointment_time = self.date
        # reminder_time = appointment_time.replace(days=-settings.REMINDER_TIME)
        date = datetime.datetime.now().date()
        # Schedule the Celery task
        from .tasks import send_sms_reminder
        ololo = appointment_time - date
        print "###############"
        print ololo
        if (appointment_time - date) == settings.REMINDER_TIME:
            result = send_sms_reminder.apply_async((self.pk), eta=settings.REMINDER_TIME)
            print "RESULT ID FROM MODEL",result.id
            return result.id


class History(models.Model):
    user_id = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    amount = models.FloatField(null=True)
    link = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
