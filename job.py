import pickle
import requests
import time
from decouple import config
from twilio.rest import Client


def send_message():
    account = config('TWILIO_ACCOUNT')
    token = config('TWILIO_TOKEN')
    client = Client(account, token)
    with open('db.bin', 'rb') as f:
        db = pickle.load(f)

    print(db['message'])
    try:
        client.messages.create(
            to=db['phone'],
            from_=config('TWILIO_PHONE'),
            body=db['message'],
            status_callback=config('STATUS_CALLBACK'))
    except requests.exceptions.ConnectionError:
        # retry to send message if there is problem connecting internet
        print("Connection error occured!")
        time.sleep(5)
        print("retrying")
        send_message()


if __name__ == '__main__':
    send_message()
