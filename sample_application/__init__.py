"""A dummy docstring."""
from flask import Flask, render_template, flash
from flask_appconfig import AppConfig
from flask_wtf import FlaskForm, RecaptchaField
from pyparsing import null_debug_action
#from flask_wtf.file import FileField
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, validators
from wtforms.validators import Required
from flask_bootstrap import Bootstrap

import pandas as pd
import os



from .nav import nav


from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, generate_account_sas, ResourceTypes, AccountSasPermissions



######run_id = dbutils.widgets.text("run_id", "1")
######run_id = dbutils.widgets.get("run_id")
######transfer_dump = dbutils.widgets.text("transfer_dump", "False")
######transfer_dump = dbutils.widgets.get("transfer_dump")
######secret_scope_name = dbutils.widgets.text(
######    "secret_scope_name", "odp-weur-sens-scope-005"
######)
######secret_scope_name = dbutils.widgets.get("secret_scope_name")
######sstorage = "lhgweurodpdevadlssens001.dfs.core.windows.net/lhg/insurance/delvag_dwh/"
######rawdir = f"abfss://raw@{sstorage}"
######stddir = f"abfss://standardized@{sstorage}"
######artdir = f"abfss://artifacts@{sstorage}"
######deltadir = f"{stddir}delta/"
######dumpdir = f"{rawdir}dump/"
######ssoutdir = f"{stddir}out/{run_id}/"
######dbutils.fs.mkdirs(f"{ssoutdir}")
######dboutdir = "/tmp/delvag"
######os.makedirs(dboutdir, exist_ok=True)

#### my part DEBUG
###AZURE_STORAGE_BLOB_URL = "https://lhgweurodpdevadlssens001.blob.core.windows.net/"
###
###
###
###
###def connect_to_stor():
###    """A dummy docstring."""
###    token_credential = DefaultAzureCredential()
###
###    blob_service_client  = BlobServiceClient(
###        account_url="https://lhgweurodpdevadlssens001.blob.core.windows.net/",
###        credential=token_credential)
###    
###    return blob_service_client
###
###
###
##########DEBUG END





# straight from the wtforms docs:
class TelephoneForm(FlaskForm):
    """A dummy docstring."""
    country_code = IntegerField('Country Code', [validators.required()])
    area_code = IntegerField('Area Code/Exchange', [validators.required()])
    number = TextField('Number')


class ExampleForm(FlaskForm):
    """A dummy docstring."""
    field1 = TextField('First Field', description='This is field one.')
    field2 = TextField('Second Field', description='This is field two.',
                       validators=[Required()])
    # hidden_field = HiddenField('You cannot see this', description='Nope')
    #recaptcha = RecaptchaField('A sample recaptcha field')
    # radio_field = RadioField('This is a radio field', choices=[
    #     ('head_radio', 'Head radio'),
    #     ('radio_76fm', "Radio '76 FM"),
    #     ('lips_106', 'Lips 106'),
    #     ('wctr', 'WCTR'),
    # ])
    # checkbox_field = BooleanField('This is a checkbox',
    #                               description='Checkboxes can be tricky.')

    # subforms
    # mobile_phone = FormField(TelephoneForm)

    # # you can change the label as well
    # office_phone = FormField(TelephoneForm, label='Your office phone')

    # ff = FileField('Sample upload')

    # submit_button = SubmitField('Submit Form')

    ##def TableForm():
    ##    return null_debug_action


    def validate_hidden_field(form, field):
        """A dummy docstring."""
        raise ValidationError('Always wrong')




def create_app(configfile=None):
    """A dummy docstring."""
    app = Flask(__name__)
    AppConfig(app, configfile)  # Flask-Appconfig is not necessary, but
                                # highly recommend =)
                                # https://github.com/mbr/flask-appconfig
    Bootstrap(app)

    # in a real app, these should be configured through Flask-Appconfig
    app.config['SECRET_KEY'] = 'devkey'
    app.config['RECAPTCHA_PUBLIC_KEY'] = \
        '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'
    
    # initialize the navigation bar
    nav.init_app(app)

    @app.route('/', methods=('GET', 'POST'))
    def index():
        #### my part DEBUG
        AZURE_STORAGE_BLOB_URL = "https://lhgweurodpdevadlssens001.blob.core.windows.net/"
        token_credential = DefaultAzureCredential()
        blob_service_client  = BlobServiceClient(
            account_url="https://lhgweurodpdevadlssens001.blob.core.windows.net/",
            credential=token_credential)

        ########## DEBUG ENDE
        form = ExampleForm()
        form.validate_on_submit()  # to get error messages to the browser
        # flash('critical message', 'critical')
        # flash('error message', 'error')
        # flash('warning message', 'warning')
        # flash('info message', 'info')
        # flash('debug message', 'debug')
        # flash('different message', 'different')
        # flash('uncategorized message')
        return render_template('index.html', form=form)

    return app

if __name__ == '__main__':
    create_app().run(debug=True)
