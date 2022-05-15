import requests
import shutil
from flask import Flask, request
from twilio.rest import Client
from twilio_utils import *
from scraper import *

account_sid, auth_token, number = load_twilio_config()
client = Client(account_sid, auth_token)
app = Flask(__name__)
meme_templates = get_template_list()

db = {}

def send_response(message, recipient):
    if (recipient in db) and (len(db[recipient]) == 3):
        template_name, top_text, bottom_text = db[recipient]
        url = f"http://apimeme.com/meme?meme={template_name}&top={top_text}&bottom={bottom_text}"
        client.messages.create(
        from_=number,
            to=recipient,
            body=message,
            media_url=url
        )
        return message + '\nURL: ' + url
    else:
        client.messages.create(
            from_=number,
            to=recipient,
            body=message,
        )
        return message

def to_template(text):
    for valid_template in meme_templates:
        if (text.lower() == ' '.join(valid_template.split('-')).lower()):
            return valid_template
    return ""

@app.route('/sms', methods=['POST'])
def incoming():
    global db
    sender_number = request.form["From"]
    message = request.form["Body"]

    # Accounting
    template_name = to_template(message)
    if (sender_number in db) or to_template(message):
        if sender_number not in db:
            db[sender_number] = []
            formatted_field = template_name
        else:
            formatted_field = '+'.join(message.split(' '))
        db[sender_number].append(formatted_field)

    # Prompting
    if sender_number not in db:
        prompt = "Choose a meme template."
    elif len(db[sender_number]) == 1:
        prompt = "What is the top text?"
    elif len(db[sender_number]) == 2:
        prompt = "What is the bottom text?"
    elif len(db[sender_number]) == 3:
        prompt = "Choose a meme template."
    send_response(prompt, sender_number)

    # Cleanup
    if (sender_number in db) and (len(db[sender_number]) == 3):
        db.pop(sender_number)

    return message

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
