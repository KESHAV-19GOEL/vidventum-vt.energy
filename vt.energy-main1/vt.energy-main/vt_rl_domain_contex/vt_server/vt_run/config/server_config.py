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

#############################################################
"""
TODO #01

1. Update the VT_SANIC_SETUP->VT_MODULE_NAME to represent the subsystem
e.g., vt_rl_user_query is a subsystem (microservice). So, the VT_SANIC_SETUP->VT_MODULE_NAME shall
reflect the module name.
VT_SANIC_SETUP->VT_MODULE_NAME = "vt-rl-user-query"

"""

"""
TODO #02

1. Update the VT_LOGGING_SETUP->VT_LOG_FILE to represent the subsystem
e.g., vt_rl_user_query is a subsystem (microservice). So, the VT_LOGGING_SETUP->VT_LOG_FILE shall
reflect the module name.
VT_LOGGING_SETUP->VT_LOG_FILE  = "vt-rl-user-query.log"

"""
#############################################################



# Used by Sanic
VT_SANIC_SETUP = ({
    'VT_MODULE_NAME': 'vt-domain-context-server',
    'VT_SANIC_SERVER_CONFIG_FILE': './vt_run/config/sanic_server_config.py'
})

# Used by application logger
# Log file ../vt_run/logs/vt-domain-context-server.log
VT_LOGGING_SETUP = ({
    'VT_LOG_DIRECTORY': '../vt_run/logs',
    'VT_LOG_FILE': 'vt-domain-context-server.log'
})

#Used by MeiliSearch for Business Data
VT_MEILI_SETUP = ({
    'VT_INDEX_NAME': 'business_data',
    'VT_BASE_URL': "http://127.0.0.1:7700"
})