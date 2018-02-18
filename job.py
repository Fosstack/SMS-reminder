import pickle
import requests
import time

from decouple import config
from twilio.rest import Client


def send_message():
    account = config('TWILIO_ACCOUNT')
    token = config('TWILIO_TOKEN')
    client = Client(account, token)
    tried = 0
    with open('db.bin', 'rb') as f:
        db = pickle.load(f)

    def send():
        nonlocal tried
        try:
            message = client.messages.create(
                to=db['phone'],
                from_=config('TWILIO_PHONE'),
                body=db['message'],
                status_callback=config('STATUS_CALLBACK'))
            sid = message.sid
            status = client.messages.get(sid).fetch().status
            time.sleep(20)
            if status != 'delivered' and tried < 5:
                tried += 1
                with open('error.log', 'wa') as f:
                    f.write(f'{ time.ctime() } { status }\
                         SMS did not send successfully\n')
                send()

        except requests.exceptions.ConnectionError:
            # retry to send message if there is problem connecting internet
            print("Connection error occured!")
            time.sleep(5)
            print("retrying")
            send()

    send()


if __name__ == '__main__':
    send_message()
