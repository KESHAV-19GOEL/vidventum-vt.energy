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
import httpx
from vt_logging.config import vt_logger_
from vt_auth.login import login
from vt_run.config.server_config import VT_SANIC_SETUP

class UserContextAPIWrapper:
    def __init__(self):
        self.base_url = VT_SANIC_SETUP['VT_SANIC_URL']
        self.client = httpx.AsyncClient()

    async def send_request(self, text):
        try:
            response = await self.client.post(
                f"{VT_SANIC_SETUP['VT_SANIC_URL']}/user-context",
                json={"text": text}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise e

    async def post_user_context(self,textList):
        tasks = []
        for text in textList:
            task = asyncio.create_task(self.send_request(text))
            tasks.append(task)
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return responses
