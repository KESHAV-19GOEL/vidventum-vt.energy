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

VT_BOT_CONFIG = ({
    'BOT_SANIC_URL':'http://127.0.0.1:8000/receive_message'
})

AGENT_CONFIG = {
    'agents': [
        {
            'Name': 'XMPPAgent1',
            'UID': 'xa001',
            'Description': 'First XMPP Agent',
            'Type': 'VT_XMPP_AGENT',
            'VT_XMPP_CONN_OBJECT': {
                'server': 'localhost',
                'Port': 5222,
                'JID': 'agent1@localhost',
                'Password_Env': 'VT_Agent_001_Pwd_Env'
            },
            'VT_AI_SERVER_CONN_OBJECT': {
                # Add AI server connection details here
            }
        },
        {
            'Name': 'XMPPAgent2',
            'UID': 'xa002',
            'Description': 'Second XMPP Agent',
            'Type': 'VT_XMPP_AGENT',
            'VT_XMPP_CONN_OBJECT': {
                'server': 'localhost',
                'Port': 5222,
                'JID': 'agent2@localhost',
                'Password_Env': 'VT_Agent_002_Pwd_Env'
            },
            'VT_AI_SERVER_CONN_OBJECT': {
                # Add AI server connection details here
            }
        },
        {
            'Name': 'XMPPAgent3',
            'UID': 'xa003',
            'Description': 'Third XMPP Agent',
            'Type': 'VT_XMPP_AGENT',
            'VT_XMPP_CONN_OBJECT': {
                'server': 'localhost',
                'Port': 5222,
                'JID': 'agent3@localhost',
                'Password_Env': 'VT_Agent_003_Pwd_Env'
            },
            'VT_AI_SERVER_CONN_OBJECT': {
                # Add AI server connection details here
            }
        }
    ]
}