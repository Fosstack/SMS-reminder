#!/usr/bin/env python

import atexit
import pickle
from datetime import datetime
from pytz import timezone

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, redirect, render_template
from forms import ReminderForm
import humanize
import phonenumbers
from phonenumbers import timezone as ptz
from job import send_message

app = Flask(__name__)
app.debug = True


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ReminderForm(request.form)
    if request.method == 'POST' and form.validate():
        with open('db.bin', 'wb') as f:
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
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            send_message,
            'cron',
            hour='7-23',  # it will run only for daytime i.e from 7AM to 11PM
            second=time_zone_time.second,
            minute=time_zone_time.minute,
            id="sms_job_id",
            timezone=time_zone)
        scheduler.start()
        # Shut down the scheduler when exiting the app
        atexit.register(lambda: scheduler.shutdown(wait=False))
        return redirect('/info')
    return render_template('home.html', form=form)


@app.route('/info')
def info():
    with open('db.bin', 'rb') as f:
        timestamp = pickle.load(f)['timestamp']
        timesince = humanize.naturaltime(datetime.now() - timestamp)
    return render_template('info.html', timesince=timesince)


if __name__ == "__main__":
    app.run(use_reloader=False)
