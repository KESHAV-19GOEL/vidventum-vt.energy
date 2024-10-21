"""Provides API Handlers for Google Translations

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
import time
from google.cloud import translate_v2 as translate

def translate_text(source_lang: str, target: str, text: str) -> dict:
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    
    translate_client = translate.Client(
        client_options={
                'api_key': os.environ.get('GOOGLE_PROJECT_API_KEY'),             
                'quota_project_id': os.environ.get('GOOGLE_PROJECT_ID')
            })

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, source_language=source_lang, target_language=target)

    return result

