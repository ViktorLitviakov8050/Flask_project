# import json
import requests
from flask_babel import _
# from app import application

def get_quote():
    r = requests.get('https://zenquotes.io/api/random')
    if r.status_code != 200:
        return _('Quote service errrorrr')
    return r.json()[0]["q"]