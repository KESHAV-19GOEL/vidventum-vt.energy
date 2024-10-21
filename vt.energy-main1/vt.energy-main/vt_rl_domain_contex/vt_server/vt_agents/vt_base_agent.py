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
class I_VTBaseAgent():
    # this serves as a base class for multiple xmpp agents
    
    async def start(self):
        # function implemented in the derived class
        pass

    async def message(self):
        # function implemented in the derived class
        pass
    