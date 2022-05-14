import requests
import shutil
from flask import Flask, request
from twilio.rest import Client
from twilio_utils import *

account_sid, auth_token, number = load_twilio_config()
client = Client(account_sid, auth_token)
app = Flask(__name__)

def send_text(recipient, message):
    client.messages.create(
        body=message,
        from_=number,
        to=recipient,
    )
    return message

def send_meme(recipient, meme_fields):
    template_name, top_text, bottom_text = meme_fields
    url = f"http://apimeme.com/meme?meme={template_name}&top={top_text}&bottom={bottom_text}"
    client.messages.create(
        from_=number,
        to=recipient,
        media_url=url
    )
    return url


@app.route('/sms', methods=['POST'])
def incoming():
    sender_number = request.form["From"]
    message = request.form["Body"]

    send_message(message, sender_number)
    return message

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
