# Download the helper library from https://www.twilio.com/docs/python/install
# Set environment variables for your credentials
# Read more at http://twil.io/secure

from django.conf import settings
from twilio.rest import Client
import random
import os

#Environment Variable 
twilio_ssid = os.environ.get('TWILIO_SSID')        # Variables not added yet
twilio_token = os.environ.get('TWILIO_TOKEN')      # Variables not added yet

class MessageHandler:
    phone_number = None
    otp =  None
    
    def __init__(self, phone_number) -> None:
        self.phone_number = phone_number

    def send_alert(self):
        # Replace these placeholders with your actual Twilio credentials
        account_sid = twilio_ssid
        auth_token = twilio_token
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            from_='+12563635113',
            body='GearfarmEssentials login detected!!',
            to=self.phone_number
        )
        
        print(message.sid)
