from wtforms import Form, StringField, validators, TextField


class ReminderForm(Form):
    phone = StringField('Phone', [validators.Length(min=13, max=13)])
    message = TextField('Message', [validators.Length(max=100)])


