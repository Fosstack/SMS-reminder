import pickle
from decouple import config
from twilio.rest import Client


def send_message():
    print('Job started!')
    account = config('TWILIO_ACCOUNT')
    token = config('TWILIO_TOKEN')
    client = Client(account, token)
    with open('db.bin', 'rb') as f:
        db = pickle.load(f)
    message = client.messages.create(
        to=db['phone'],
        from_=config('TWILIO_PHONE'),
        body=db['message'],
        status_callback='http://d5fd4d4d.ngrok.io')


if __name__ == '__main__':
    send_message()
