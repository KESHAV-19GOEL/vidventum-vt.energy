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

import os
import logging
from logging.config import dictConfig
from sanic import Request
from sanic.exceptions import SanicException
from vt_run.config.server_config import VT_LOGGING_SETUP

# Log file ../vt_run/logs/vt-api-server.log
app_root_ = os.path.dirname(os.path.abspath(__file__))
log_dir_ = os.path.join(app_root_, VT_LOGGING_SETUP['VT_LOG_DIRECTORY'])
if not os.path.exists(log_dir_):
    os.mkdir(log_dir_)

log_file_ = os.path.join(log_dir_, VT_LOGGING_SETUP['VT_LOG_FILE'])

# More information about the request, such as the IP address, may help debugging some errors.
class VtAPIRequestFormatter():
    # Log parameters
    request_id_ = ""
    remote_addr_ = ""
    host_ = ""
    api_ = ""

    def format(self, request: Request):
        try:            
            self.request_id_ = str(request.id)
            self.remote_addr_ = str(request.remote_addr)
            self.host_ = str(request.ip)
            self.api_ = request.method + " " + request.url
        
        except SanicException:
            # Logging has no Request object. Let's initialize the logging parameters.
            self.request_id_ = None
            self.remote_addr_ = None
            self.host_ = None
            self.api_ = None

        log_req_ = f'ID: {self.request_id_} - Remote Address: {self.remote_addr_} - Host: {self.host_ } - API: {self.api_}' 
        
        return log_req_


VT_REQUEST_LOGGING_FORMAT = (
    
    '%(asctime)s - [%(levelname)s] [Module: %(module)s] [Logger: %(name)s] '
    '[ID: %(request_id)s] [Remote: %(remote_addr)s] [Host: %(host)s] [API: %(request)s] - %(message)s'
)

# More information about the request, such as the IP address, may help debugging some errors.
class VtSanicRequestFormatter(logging.Formatter):
    def format(self, record):
        try:
            request = Request.get_current()            
            record.request_id = str(request.id)
            record.remote_addr = str(request.remote_addr)
            record.host = str(request.ip)
            record.request = request.method + " " + request.url
        
        except SanicException:
            # Logging has no Request object. Let's initialize the logging parameters.
            record.request_id = ""
            record.remote_addr = ""
            record.host = ""
            record.request = ""

        return super().format(record)

vt_sanic_req_formatter_= VtSanicRequestFormatter(
    VT_REQUEST_LOGGING_FORMAT
)

# Python Logging Config.
dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters':
        {
            'standard':
                {
                    'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
                },
            'sanic':
                {
                    '()': lambda: vt_sanic_req_formatter_
                }  
        },
    'handlers':
        {
            'vt-log-handler':
                {
                    'level': 'ERROR',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': log_file_,
                    'formatter': 'sanic',
                    'maxBytes': 10000000,
                    'backupCount': 10
                }
        },
    'loggers':
        {
            'vt-logger':
                {
                    'handlers': ['vt-log-handler'],
                    'level': 'ERROR',
                    'propagate': False
                }
        },
    'root':
        {
            'level': 'DEBUG',
            'handlers': ['vt-log-handler']
        }
})

# APIs usr this logger.
vt_logger_ = logging.getLogger('vt-logger')

