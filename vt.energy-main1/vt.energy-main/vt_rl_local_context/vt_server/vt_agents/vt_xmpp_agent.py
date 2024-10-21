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
import requests
import ssl 
from vt_run.config.agent_config import VT_AGENT_CONFIG ,VT_BOT_CONFIG 
from slixmpp import ClientXMPP
from slixmpp.exceptions import IqError, IqTimeout
from vt_logging.config import vt_logger_


class VTXMPPAgent(ClientXMPP):
    def __init__(self, agent_config):
        # Extracting the necessary details from the config
        self.name = agent_config['name']
        xmpp_config = agent_config['connection_objects']['VT_XMPP_CONN_OBJECT']
        jid = xmpp_config['jid']
        password = xmpp_config['password']
        
        # Initialize the ClientXMPP with JID and password
        super().__init__(jid, password)
        
        # Add event handlers for session start and message received 
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        
        # Register necessary XMPP plugins 
        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0199')  # XMPP Ping
        self.register_plugin('xep_0092')
        
        # Use a more secure SSL version for OpenFire
        self.ssl_version = ssl.PROTOCOL_TLS_CLIENT
        
        # Disable SSL certificate verification
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

    async def start(self, event):
        # Send presence to indicate the bot is online
        self.send_presence()
        try:
            # Try to get the roster
            await self.get_roster()
        except IqError as err:
            vt_logger_.info(f'{self.name}: There was an error getting the roster')
            vt_logger_.info(err.iq['error']['condition'])
            self.disconnect()
        except IqTimeout:
            vt_logger_.info(f'{self.name}: Server is taking too long to respond')
            self.disconnect()

    def message(self, msg):
        # Handle incoming messages
        if msg['type'] in ('chat', 'normal'):
            # Echo the received message back to the sender            
            # msg.reply("from agent2- %(body)s" % msg).send()
            msg.reply(f"from {self.name} - {msg['body']}").send()
            # Send the message to the Sanic server
            self.send_to_sanic(msg['body'])

    def send_to_sanic(self, message):
            # Send the message to the Sanic server
            sanic_url = VT_BOT_CONFIG['BOT_SANIC_URL']
            data = {'message': message,'name':self.name}
            requests.post(sanic_url, json=data)
            