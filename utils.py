from datetime import datetime

import humanize
import pickle
from decouple import config
from twilio.rest import Client


def get_natural_timesince():
    with open('db.bin', 'rb') as f:
        timestamp = pickle.load(f)['timestamp']
        timesince = humanize.naturaltime(datetime.now() - timestamp)
    return timesince


def get_natural_timedelta():
    with open('db.bin', 'rb') as f:
        timestamp = pickle.load(f)['timestamp']
        timesince = humanize.naturaldelta(datetime.now() - timestamp)
    return timesince


def twilio_authenticate():
    account = config('TWILIO_ACCOUNT')
    token = config('TWILIO_TOKEN')
    client = Client(account, token)
    return client
