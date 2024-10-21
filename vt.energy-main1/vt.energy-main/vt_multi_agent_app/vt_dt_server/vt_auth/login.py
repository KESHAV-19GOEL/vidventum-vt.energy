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

import jwt
import calendar
import datetime
from sanic import Blueprint, text

login = Blueprint("login", url_prefix="/login")

@login.post("/")
async def do_login(request):
    token = jwt.encode({"name": request.app.config.VT_NAME}, request.app.config.SECRET,  algorithm='HS256')
    return text(token)
