# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.conf import settings

import arrow

from twilio.rest import Client
from .views import .
from .models import User, Bill
# from .models import Bill

account_sid = "ACef32059d9f6f7000f77fa1d03213bb3e" # Your Account SID from www.twilio.com/console
auth_token  = "79b895f4f4ad868519a23b194268527a"  # Your Auth Token from www.twilio.com/console
client = Client(account_sid, auth_token)

app = Celery('tasks', broker='amqp://guest:guest@localhost:5672//')

@app.shared_task
def send_sms_reminder(bill_id):
    """Send a reminder to a phone using Twilio SMS"""
    # Get our appointment from the database
    try:
        bill = Bill.objects.get(pk=bill_id)
    except Bill.DoesNotExist:
        # The appointment we were trying to remind someone about
        # has been deleted, so we don't need to do anything
        return

    bill_time = arrow.get(bill.date)
    body = 'Hi {0}. You have a bill coming up at {1}.'.format(
        user.first_name,
        bill_time.format("m-d-Y")
    )

    message = client.messages.create(
        body=body,
        to=user.phone_number,
        from_=settings.TWILIO_NUMBER,
    )

#
# @shared_task
# def mul(x, y):
#     return x * y
#
#
# @shared_task
# def xsum(numbers):
#     return sum(numbers)
