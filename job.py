import pickle
import requests
import time

from decouple import config

from utils import twilio_authenticate, get_natural_timedelta


def send_message():
    client = twilio_authenticate()
    tried = 0
    with open('db.bin', 'rb') as f:
        db = pickle.load(f)

    def send():
        nonlocal tried
        running_time = get_natural_timedelta()
        # the user will get the time for which the service is running
        body = f"{db['message']}\nservice running for {running_time}"

        try:
            message = client.messages.create(
                to=db['phone'],
                from_=config('TWILIO_PHONE'),
                body=body,
                status_callback=config('STATUS_CALLBACK'))
            sid = message.sid
            status = client.messages.get(sid).fetch().status
            time.sleep(20)
            if status not in ['sent', 'delivered'] and tried < 5:
                tried += 1
                with open('error.log', 'a+') as f:
                    f.write(f'{ time.ctime() } { status }\
                    SMS did not send successfully\n')
                # saving the error log in "error.log" file in root directory
                send()
                time.sleep(20)
                # the instant SMS status is likely to be "queued", therefore
                # trying 20 seconds after sending message, and doing it
                # for maximum five times
                status = client.messages.get(sid).fetch().status

        except requests.exceptions.ConnectionError:
            # retry to send message if there is problem connecting internet
            print("Connection error occured!")
            time.sleep(5)
            print("retrying")
            send()

    send()


if __name__ == '__main__':
    send_message()
