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
import requests
import ssl
from .vt_base_agent import I_VTBaseAgent
from vt_logging.vt_botlogger_ import vt_botlogger_ 
from vt_run.config.agent_config import agent_config ,VT_BOT_CONFIG 
from slixmpp import ClientXMPP
from slixmpp.exceptions import IqError, IqTimeout

class VTXMPPAgent(I_VTBaseAgent,ClientXMPP):
    """
    VTXMPPAgent is an XMPP client agent for handling messaging via the XMPP protocol.

    Attributes:
        name (str): Name of the agent.
        jid (str): Jabber ID (JID) for the XMPP account.
        password (str): Password for the XMPP account and send the message to the sanic server.

    Methods:
        start(event): Called when the XMPP session starts.
        message(msg): Handles incoming messages.
    """
    def __init__(self, config, logger):
        """
        Initialize the VTXMPPAgent with configuration details.

        Parameters:
            agent_config (dict): Configuration dictionary for the agent.

        Raises:
            ValueError: If the environment variable for the password is not set.
        """
        self.logger=logger
        self.config = config
        self.uid = config.get('UID')
        self.description = config.get('Description')
        self.type = config.get('Type')
        self.name = config['Name']
        xmpp_config = config['Connection Objects']['VT_XMPP_CONN_OBJECT']
        jid = xmpp_config['JID']
        password_env_variable = xmpp_config.get('Password')
        password = os.getenv(password_env_variable,default=None)
        
        if not password:
            raise ValueError("Agent JID and/or Password is not set.")
        
        # Initialize the ClientXMPP with JID and password
        ClientXMPP.__init__(self,jid, password)
        
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
    
    # overriding start function from the I_VTBaseAgent 
    async def start(self, event):
        """
        Called when the XMPP session starts.

        Parameters:
            event: The event object for session start.
        """
        # Send presence to indicate the bot is online
        self.send_presence()
        try:
            # Try to get the roster
            await self.get_roster()
        except IqError as err:
            self.logger.error(f'{self.name}: There was an error getting the roster')
            self.logger.error(err.iq['error']['condition'])
            self.disconnect()
        except IqTimeout:
            self.logger.error(f'{self.name}: Server is taking too long to respond')
            self.disconnect()
    
    # overriding message function from the I_VTBaseAgent
    def message(self, msg):
        """
        Handles incoming messages.

        Parameters:
            msg: The incoming message object.
        """
        sanic_url = VT_BOT_CONFIG['BOT_SANIC_URL']
        if msg['type'] in ('chat', 'normal'):
            # Echo the received message back to the sender            
            msg.reply("%(body)s" % msg).send()
            message = msg['body']
            # Send the message to the Sanic server      
            data = {'message': message,'name':self.name}
            requests.post(sanic_url, json=data)
            