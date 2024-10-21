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

1. Update the VT_NAME to represent the subsystem
e.g., vt_rl_user_query is a subsystem (microservice). So, the VT_NAME shall
reflect the module name.
VT_NAME = "VT.ENERGY_RL_USER_QUERY_SERVER_v0.1.0"

"""
#############################################################


# Used by JWT
VT_NAME = "VT.ENERGY_BOT_SERVER_v0.1.0"

# Used by Sanic
REQUEST_TIMEOUT=60

#
# Password generator: openssl rand -base64 42 or lenght of the password.
#
# Used by JWT
SECRET = "7qshKCvohK9uSekOhvhbWGuIZ2Iee0ZufzNshdiocMPOamrxUt4CebLL"
