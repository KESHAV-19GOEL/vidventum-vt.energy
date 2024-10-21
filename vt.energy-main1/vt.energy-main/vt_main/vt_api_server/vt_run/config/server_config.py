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
    'VT_MODULE_NAME': 'vt-main-server',
    'VT_SANIC_SERVER_CONFIG_FILE': './vt_run/config/sanic_server_config.py'
})

# Used by application logger
# Log file ../vt_run/logs/vt-main-server.log
VT_LOGGING_SETUP = ({
    'VT_LOG_DIRECTORY': '../vt_run/logs',
    'VT_LOG_FILE': 'vt-main-server.log'
})
