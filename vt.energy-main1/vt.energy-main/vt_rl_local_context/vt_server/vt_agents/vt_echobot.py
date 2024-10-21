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
from slixmpp.exceptions import IqError,IqTimeout
import ssl
import asyncio
import os 
import logging

jid = "admin@ayananshuscar"
password = "admin"
logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s') 

vt_logger = logging.getLogger('vt_logger') 

class EchoBot(ClientXMPP): 

    def __init__(self, jid, password): 

        super().__init__(jid, password) 

        self.add_event_handler("session_start", self.start) 

        self.add_event_handler("message", self.message) 


        self.ssl_version = ssl.PROTOCOL_TLS_CLIENT 

         

        # Disable SSL certificate verification 

        self.ssl_context = ssl.create_default_context() 

        self.ssl_context.check_hostname = False 

        self.ssl_context.verify_mode = ssl.CERT_NONE 

 

    async def start(self, event): 

        self.send_presence() 

        try: 

            await self.get_roster() 

        except IqError as err: 

            vt_logger.error('There was an error getting the roster') 

            vt_logger.error(err.iq['error']['condition']) 

            self.disconnect() 

        except IqTimeout: 

            vt_logger.error('Server is taking too long to respond') 

            self.disconnect() 

 

    def message(self, msg): 

        if msg['type'] in ('chat', 'normal'): 

            msg.reply("%(body)s" % msg).send() 

if __name__ == '__main__': 
    xmpp = EchoBot( jid, password)
    xmpp.connect(use_ssl=False, force_starttls=False, disable_starttls=True)
    xmpp.process(forever=True)
