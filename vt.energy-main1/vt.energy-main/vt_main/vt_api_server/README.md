```
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
```

# Installation

## Prerequisites

1. Setup Python Virtual Environment
2. Python version: 3.10.12
3. Install poetry (package dependency manager)
4. You can find pyproject.toml in the root of the project.
5. `poetry install`

## Running the webserver

### Development / Debug 
```
sanic server:app --fast --no-access-logs --debug --auto-reload
```

### Production
```
sanic server:app --fast --no-access-logs
```

### Directory structure

```
.
├── README.md
├── server.py
├── vt_advanced
│   └── README.txt
├── vt_api_handlers
│   └── languages
│       ├── google.py
├── vt_auth
│   ├── auth.py
│   ├── login.py
├── vt_basics
│   ├── custom_requests.py
├── vt_logging
│   ├── config.py
├── vt_run
│   ├── config
│   │   ├── sanic_server_config.py
│   │   └── server_config.py
│   └── logs
└── vt_testing    

```

```
vt_run has runtime config and target log directories.

The vt_run/config directory holds all application config settings for both development and prodution as well.
```

### JWT (API authentication)

```
vt_run/config/ has a SECRET. It will be used to generate JWT tokens.

For Testing:
JWT token can be generated http://<host>/login
The above API returns a JWT token. Use this token to access the secure/protected routes.
```

```
curl http://<host>/secure -i -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.e30.rjxS7ztIGt5tpiRWS8BGLUqjQFca4QOetHcZTi061DE"
```

## Google Translation

### Useful links

```
https://cloud.google.com/translate/docs/reference/libraries/v2/python
https://console.cloud.google.com/apis/library/translate.googleapis.com?project=vt-ai-lang-v1
https://cloud.google.com/translate/docs/basic/translate-text-basic
https://cloud.google.com/docs/authentication/external/set-up-adc
https://g.co/cloud/translate/v2/translate-reference#supported_languages

```

