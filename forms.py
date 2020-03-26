import re

from wtforms import Form, StringField, validators, TextField

from utils import twilio_authenticate


class ReminderForm(Form):
    phone = StringField('Phone', [
        validators.Length(
            min=13, max=13, message='Enter a valid phone number')
    ])
    message = TextField('Message', [validators.Length(max=100)])

    @staticmethod
    def validate_phone(field):
        rule = re.compile(r'(^[+0-9]{1,3})*([0-9]{10,11}$)')
        if not rule.search(field.data):
            return False

        client = twilio_authenticate()
        if field.data not in [
                i.phone_number for i in client.outgoing_caller_ids.list()
        ]:
            raise validators.ValidationError(
                "Your phone nubmer is not verified\
                . Contact admin to add your phone number.")

        return True
