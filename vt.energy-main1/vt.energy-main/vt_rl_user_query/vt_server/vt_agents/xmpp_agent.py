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

from slixmpp import ClientXMPP
from .base_agent import VTBaseAgent
import os
import asyncio
import threading
from vt_logging.config import vt_logger_
import requests
import ssl
from slixmpp.exceptions import IqError, IqTimeout
from vt_run.config.agent_config import VT_BOT_CONFIG

class VTXMPPAgent(VTBaseAgent, ClientXMPP):
    def __init__(self, config, logger):
        VTBaseAgent.__init__(self, config, logger)
        self.name = config.get('Name', 'UnnamedAgent')
        self.uid = config.get('UID', 'UnknownUID')
        self.description = config.get('Description', 'No description provided')
        self.type = config.get('Type', 'UnknownType')
        self.xmpp_config = config.get('VT_XMPP_CONN_OBJECT', {})
        jid = self.xmpp_config.get('JID')
        password_env = self.xmpp_config.get('Password_Env')
        password = os.getenv(password_env)
        if not password:
            error_msg = f"Password environment variable {password_env} not set for agent {self.name}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        ClientXMPP.__init__(self, jid, password)
        
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        self.add_event_handler("connection_failed", self.on_connection_failed)
        self.add_event_handler("disconnected", self.on_disconnected)
        
        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0199')  # XMPP Ping
        self.register_plugin('xep_0092')
        
        self.ssl_version = ssl.PROTOCOL_TLS_CLIENT
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        
        self.running = False
        logger.info(f"Initializing XMPP Agent: {self.name}")

    async def start(self, event):
        self.send_presence()
        try:
            await self.get_roster()
        except IqError as err:
            self.logger.error(f'{self.name}: There was an error getting the roster')
            self.logger.error(err.iq['error']['condition'])
            self.disconnect()
        except IqTimeout:
            self.logger.error(f'{self.name}: Server is taking too long to respond')
            self.disconnect()

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            msg.reply(f"Echo: {msg['body']}").send()
            self.logger.info(f"XMPP Agent {self.name} echoed message: {msg['body']}")
            
            # Send the message to the Sanic server
            sanic_url = VT_BOT_CONFIG['BOT_SANIC_URL']
            data = {'message': msg['body'], 'name': self.name}
            requests.post(sanic_url, json=data)

    def on_connection_failed(self, event):
        self.logger.error(f"Connection failed for {self.name}: {event}")

    def on_disconnected(self, event):
        self.logger.info(f"{self.name} disconnected: {event}")