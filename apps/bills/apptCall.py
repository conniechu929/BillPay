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

print(message.sid)
