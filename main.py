#!/usr/bin/env python
import atexit
import pickle
import time

from flask import Flask, request, redirect, render_template
from forms import ReminderForm

import humanize
from apscheduler.schedulers.background import BackgroundScheduler

from job import send_message

app = Flask(__name__)
app.debug = True


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ReminderForm(request.form)
    if request.method == 'POST' and form.validate():
        with open('db.bin', 'wb') as f:
            pickle.dump({
                'phone': request.form['phone'],
                'message': request.form['message'],
                'timestamp': time.time()
            }, f)

        scheduler = BackgroundScheduler()
        scheduler.add_job(
            send_message, 'interval', seconds=30, id="sms_job_id")
        scheduler.start()
        # Shut down the scheduler when exiting the app
        atexit.register(lambda: scheduler.shutdown(wait=False))
        return redirect('/info')
    return render_template('home.html', form=form)


@app.route('/info')
def info():
    with open('db.bin', 'rb') as f:
        timestamp = pickle.load(f)['timestamp']
        timesince = humanize.naturaltime(time.time() - timestamp)
    return render_template('info.html', timesince=timesince)


if __name__ == "__main__":
    app.run(use_reloader=False)
