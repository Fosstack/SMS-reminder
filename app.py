#!/usr/bin/env python

import atexit
import pickle
from datetime import datetime
from pytz import timezone

from apscheduler.schedulers.background import BackgroundScheduler
from decouple import config
from flask import Flask, request, redirect, render_template
from forms import ReminderForm
import phonenumbers
from phonenumbers import timezone as ptz
from job import send_message
from utils import get_natural_timesince

app = Flask(__name__)
# Debug set to False in development
app.debug = config('DEBUG', default=False, cast=bool)


@app.route('/', methods=['GET', 'POST'])
def index():

    form = ReminderForm(request.form)
    if request.method == 'POST' and form.validate():
        with open('db.bin', 'wb') as f:

            # getting timezone with phone number
            raw_phone_number = request.form['phone']
            phone_number = phonenumbers.parse(raw_phone_number)
            time_zone = ptz.time_zones_for_number(phone_number)[0]

            pickle.dump({
                'phone': request.form['phone'],
                'message': request.form['message'],
                'timestamp': datetime.now(),
                'time_zone': time_zone
            }, f)

        _time_zone = timezone(time_zone)
        time_zone_time = datetime.now(_time_zone)

        # timezone helps determining the night hours of user's country
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            send_message,
            'cron',
            hour='7-23',
            second=time_zone_time.second,
            minute=time_zone_time.minute,
            id="sms_job_id",
            timezone=time_zone)
        # the above cronjob will run forever every hour from the time it called
        scheduler.start()
        # Shut down the scheduler when exiting the app
        atexit.register(lambda: scheduler.shutdown(wait=False))
        return redirect('/info')
    return render_template('home.html', form=form)


@app.route('/info')
def info():
    return render_template('info.html', timesince=get_natural_timesince())


if __name__ == "__main__":
    app.run()
