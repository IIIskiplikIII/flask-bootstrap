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
import requests
import json
import plotly_express as px

from .plotly_graph import PlotlyGraph

from .nav import nav
#from .line_plot import mylineplot


from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, generate_account_sas, ResourceTypes, AccountSasPermissions


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
    
    @app.route('/line_plot', methods=('GET', 'POST'))
    def line_plot():
        return render_template('line_plot.html')

    @app.route('/line_plot_test', methods=['GET', 'POST'])
    def line_plot_test():

        df = px.data.gapminder()

        plotly_graph = PlotlyGraph("gdpPercap","lifeExp")
        graph_json = plotly_graph.get_json_graph(df)

        return render_template(
            'line_plot_test.html',graph_json = graph_json)

    return app

if __name__ == '__main__':
    create_app().run(debug=True)
