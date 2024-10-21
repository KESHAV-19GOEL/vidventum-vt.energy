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

import threading
from abc import ABC, abstractmethod

class VTBaseAgent(ABC):
    def __init__(self, config, logger):
        # super().__init__()
        self.config = config
        self.logger = logger
        self.name = None
        self.uid = None
        self.description = None
        self.type = None

    async def start(self):
        # function implemented in the derived class
        pass

    async def message(self):
        # function implemented in the derived class
        pass