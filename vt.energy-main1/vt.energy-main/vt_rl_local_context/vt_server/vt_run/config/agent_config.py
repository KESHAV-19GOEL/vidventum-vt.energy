#==========================LICENSE NOTICE==========================
#
# Copyright (c) 2024 Vidcentum Technologies Pvt Ltd, India.
# License: Refer to LICENSE file of the software package.
# Email: support@vidcentum.com
# Website: https://vidcentum.com
#
##=======================END LICENSE NOTICE========================

import os

# Configuration for the Sanic server URL
VT_BOT_CONFIG = ({
    'BOT_SANIC_URL':'http://127.0.0.1:8000/endpoint'
})

VT_AGENT_CONFIG = [
    {
        "name": "Agent1",
        "uid": "agent1",
        "description": "First XMPP agent",
        "type": "VT_XMPP_AGENT",
        "connection_objects": {
            "VT_XMPP_CONN_OBJECT":
            {
                "type": "VT_XMPP_CONN_OBJECT",
                "server": "ayananshuscar",
                "port": 5222,
                "jid": "agent1@ayananshuscar",
                "password": "ayanAgent1"#os.getenv("AGENT1_PASSWORD") #
            },
        }
    },
    {
        "name": "Agent2",
        "uid": "agent2",
        "description": "Second XMPP agent",
        "type": "VT_XMPP_AGENT",
        "connection_objects": {
            "VT_XMPP_CONN_OBJECT":
            {
                "type": "VT_XMPP_CONN_OBJECT",
                "server": "ayananshuscar",
                "port": 5222,
                "jid": "agent2@ayananshuscar",
                "password": "ayanAgent2"#os.getenv("AGENT2_PASSWORD") #
            },
        }
    },
    {
        "name": "Agent3",
        "uid": "agent3",
        "description": "Third XMPP agent",
        "type": "VT_XMPP_AGENT",
        "connection_objects": {
            "VT_XMPP_CONN_OBJECT":
            {
                "type": "VT_XMPP_CONN_OBJECT",
                "server": "ayananshuscar",
                "port": 5222,
                "jid": "agent3@ayananshuscar",
                "password": "ayanAgent3"#os.getenv("AGENT3_PASSWORD") 
            },
        }
    }
]
