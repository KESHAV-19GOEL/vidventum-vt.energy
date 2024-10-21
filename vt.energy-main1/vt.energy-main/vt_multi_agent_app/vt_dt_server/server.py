"""
#==========================LICENSE NOTICE==========================
#
# Copyright (c) 2024 Vidcentum Technologies Pvt Ltd, India.
# License: Refer to LICENSE file of the software package.
# Email: support@vidcentum.com
# Website: https://vidcentum.com
#
##=======================END LICENSE NOTICE========================
"""

import os
import time
import asyncio
import nats
from sanic import Sanic
from sanic.response import text
from sanic.response import json
from sanic.request import Request
from sanic.exceptions import SanicException
from vt_basics.custom_requests import VtNanoSecondRequest
from vt_logging.config import vt_logger_
from vt_auth.auth import protected
from vt_auth.login import login
from vt_api_handlers.languages.google import translate_text
from vt_run.config.server_config import VT_SANIC_SETUP


# Create API Server App and initialize with config file.
app = Sanic(VT_SANIC_SETUP['VT_MODULE_NAME'], request_class=VtNanoSecondRequest)
app.update_config(VT_SANIC_SETUP['VT_SANIC_SERVER_CONFIG_FILE'])

app.blueprint(login)

# APIs

###############
# THE FOLLOWING APIs ARE FOR LEEARNING PURPOSE.
###############

@app.get("/")
async def hello_api(request: Request):
    # First log the Request received
    vt_logger_.error(f'Hello World API serviced.')
    return text(f'Hello World API serviced. No API token needed.')


@app.post("/secure")
@protected
async def secure_api(request: Request):
    # First log the Request received
    vt_logger_.error(f'To go fast, you must be fast!')
    return text(f'To go fast, you must be fast!\n\r')


@app.post("/wa-alert-field-staff")
@protected
async def alert_field_staff(request: Request):
    # First log the Request received
    vt_logger_.error(f'Filed Alert Job Created!')

    # Connect to NATS!
    nc = await nats.connect("localhost")

    # Publish a message to 'vt.wa.message'
    await nc.publish("vt.wa.message", request.body)

    # Make sure all published messages have reached the server
    await nc.flush()

    # Close NATS connection
    await nc.close()

    return text(f'Field Alert Job Created!\n\r')


@app.post("/translate-it-2-en")
@protected
async def translate_it_2_en(request: Request):
    result = translate_text('it', 'en', request.json['text'])    
    return text(f'{result["translatedText"]}\n\r')


@app.post("/translate-en-2-it")
@protected
async def translate_en_2_it(request: Request):
    result = translate_text('en', 'it', request.json['text'])    
    return text(f'{result["translatedText"]}\n\r')


###############
# THE FOLLOWING APIs IMPLEMENT THE MODULE FUNCTIONALITY. 
###############

#
# Module APIs
#


if __name__ == "__main__":
    app.run(debug=False, access_log=False, fast=True)

