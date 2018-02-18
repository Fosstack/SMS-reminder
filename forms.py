import re
from wtforms import Form, StringField, validators, TextField


class ReminderForm(Form):
    phone = StringField('Phone', [
        validators.Length(
            min=13, max=13, message='Enter a valid phone number')
    ])
    message = TextField('Message', [validators.Length(max=100)])

    def validate_phone(self, field):
        rule = re.compile(r'(^[+0-9]{1,3})*([0-9]{10,11}$)')
        if not rule.search(field.data):
            return False
        return True
