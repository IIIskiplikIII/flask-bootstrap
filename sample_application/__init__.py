"""A dummy docstring."""
import requests
from flask import Flask, render_template, flash, session, request, redirect, url_for
from flask_appconfig import AppConfig
from flask_wtf import FlaskForm, RecaptchaField
from pyparsing import null_debug_action
#from flask_wtf.file import FileField
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, validators
from wtforms.validators import Required
from flask_bootstrap import Bootstrap
from flask_session import Session
import msal
from sample_application import app_config

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
        if not session.get("user"):
            return redirect(url_for("login"))
        return render_template('index.html', user=session["user"], version=msal.__version__, form=form)
        # form = ExampleForm()
        # form.validate_on_submit()  # to get error messages to the browser
        # flash('critical message', 'critical')
        # flash('error message', 'error')
        # flash('warning message', 'warning')
        # flash('info message', 'info')
        # flash('debug message', 'debug')
        # flash('different message', 'different')
        # flash('uncategorized message')
        # return render_template('index.html', form=form)

    @app.route("/login")
    def login():
        # Technically we could use empty list [] as scopes to do just sign in,
        # here we choose to also collect end user consent upfront
        session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE)
        return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)

    @app.route(app_config.REDIRECT_PATH)  # Its absolute URL must match your app's redirect_uri set in AAD
    def authorized():
        try:
            cache = _load_cache()
            result = _build_msal_app(cache=cache).acquire_token_by_auth_code_flow(
                session.get("flow", {}), request.args)
            if "error" in result:
                return render_template("auth_error.html", result=result)
            session["user"] = result.get("id_token_claims")
            _save_cache(cache)
        except ValueError:  # Usually caused by CSRF
            pass  # Simply ignore them
        return redirect(url_for("index"))
    
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




def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache

def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()


def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        app_config.CLIENT_ID, authority=authority or app_config.AUTHORITY,
        client_credential=app_config.CLIENT_SECRET, token_cache=cache)


def _build_auth_code_flow(authority=None, scopes=None):
    return _build_msal_app(authority=authority).initiate_auth_code_flow(
        scopes or [],
        redirect_uri=url_for("authorized", _external=True))


if __name__ == '__main__':
    create_app().run(debug=True)