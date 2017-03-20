from __future__ import absolute_import

from celery import shared_task
from django.conf import settings

import arrow

from twilio.rest import Client
from .views import .
from .models import User
from .models import Bill

account_sid = "ACef32059d9f6f7000f77fa1d03213bb3e" # Your Account SID from www.twilio.com/console
auth_token  = "79b895f4f4ad868519a23b194268527a"  # Your Auth Token from www.twilio.com/console

client = Client(account_sid, auth_token)

message = client.messages.create(body="Hello from Python",
    to="+14158109387",    # Replace with your phone number
    from_="+14156718046") # Replace with your Twilio number

# print(message.sid)

# @shared_task
# def send_sms_reminder(appointment_id):
#     """Send a reminder to a phone using Twilio SMS"""
#     # Get our appointment from the database
#     try:
#         appointment = Appointment.objects.get(pk=appointment_id)
#     except Appointment.DoesNotExist:
#         # The appointment we were trying to remind someone about
#         # has been deleted, so we don't need to do anything
#         return
#
#     appointment_time = arrow.get(appointment.time, appointment.time_zone.zone)
#     body = 'Hi {0}. You have an appointment coming up at {1}.'.format(
#         appointment.name,
#         appointment_time.format('h:mm a')
#     )
#
#     message = client.messages.create(
#         body=body,
#         to=appointment.phone_number,
#         from_=settings.TWILIO_NUMBER,
#     )
