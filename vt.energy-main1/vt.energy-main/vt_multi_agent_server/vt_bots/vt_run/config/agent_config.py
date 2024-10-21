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

# Configuration for the Sanic server URL
VT_BOT_CONFIG = ({
    'BOT_SANIC_URL':'http://127.0.0.1:8000/send_message_to_resolution_layer'
})

# Configuration for different XMPP agents
agent_config = [
    {
        "Name": "Agent1",
        "UID": "001",
        "Description": "First XMPP Agent",
        "Type": "VT_XMPP_AGENT",
        "Connection Objects": {
            "VT_XMPP_CONN_OBJECT": {
                "server": "amanlocalhost.com",
                "Port": 5222,
                "JID": "echobot@amanlocalhost.com",
                "Password": "xmpp_bot1"
            },
            "VT_AI_SERVER_CONN_OBJECT": {}
        }
    },
    {
        "Name": "Agent2",
        "UID": "002",
        "Description": "Second XMPP Agent",
        "Type": "VT_XMPP_AGENT",
        "Connection Objects": {
            "VT_XMPP_CONN_OBJECT": {
                "server": "amanlocalhost.com",
                "Port": 5222,
                "JID": "echobot2@amanlocalhost.com",
                "Password": "xmpp_bot2"
            },
            "VT_AI_SERVER_CONN_OBJECT": {}
        }
    },
    {
        "Name": "Agent3",
        "UID": "003",
        "Description": "Third XMPP Agent",
        "Type": "VT_XMPP_AGENT",
        "Connection Objects": {
            "VT_XMPP_CONN_OBJECT": {
                "server": "amanlocalhost.com",
                "Port": 5222,
                "JID": "echobot3@amanlocalhost.com",
                "Password": "xmpp_bot3"
            },
            "VT_AI_SERVER_CONN_OBJECT": {}
        }
    }
]
