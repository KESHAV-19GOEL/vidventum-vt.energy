

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

import time
from sanic.request import Request
from vt_logging.config import vt_logger_

# Custom Request Handler
class VtNanoSecondRequest(Request):
    @classmethod
    def generate_id(*_):
        return time.time_ns()
