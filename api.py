import requests
import shutil
from flask import Flask, request
from twilio.rest import Client
from twilio_utils import *

account_sid, auth_token, number = load_twilio_config()
client = Client(account_sid, auth_token)
app = Flask(__name__)

def get_meme(template_name, top_text, bottom_text):
    url = f"http://apimeme.com/meme?meme={template_name}&top={top_text}&bottom={bottom_text}"
    response = requests.request("GET", url, stream=True)
    response.raw.decode_content = True
    with open("img.jpg", "wb") as file:
        shutil.copyfileobj(response.raw, file)
    return response.raw

def send_message(message, recipient):
    client.messages.create(
        body=message,
        from_=number,
        to=recipient,
        media_url="https://demo.twilio.com/owl.png"
    )
    return message

@app.route('/sms', methods=['POST'])
def incoming():
    # get_meme("10-Guy", "TOP", "BOTTOM")
    sender_number = request.form["From"]
    message = request.form["Body"]

    send_message(message, sender_number)
    return message

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
