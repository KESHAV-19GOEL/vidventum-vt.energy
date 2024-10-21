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
import time
import sys
import httpx
import asyncio
import requests
import json as json_lib
import threading
import contextlib

from sanic import Sanic
from sanic.response import text, json
from sanic.request import Request
from sanic_ext import Extend, openapi
from user_context_wrapper import UserContextAPIWrapper

from vt_basics.custom_requests import VtNanoSecondRequest
from vt_logging.config import vt_logger_
from vt_auth.auth import protected
from vt_auth.login import login
from vt_run.config.server_config import VT_SANIC_SETUP
from vt_run.config.agent_config import VT_AGENT_CONFIG
from vt_agents.vt_xmpp_agent import VTXMPPAgent

# Global variables to hold bot instances and event loops
bot_instances = []
bot_event_loops = []
bot_threads = []
# Event to signal threads to stop
stop_event = threading.Event()

# Create API Server App and initialize with config file.
app = Sanic(VT_SANIC_SETUP['VT_MODULE_NAME'], request_class=VtNanoSecondRequest)
app.update_config(VT_SANIC_SETUP['VT_SANIC_SERVER_CONFIG_FILE'])
app.config.update({
    'VT_MEILI_URL': VT_SANIC_SETUP['VT_MEILI_URL'],
    'VT_INDEX_NAME': VT_SANIC_SETUP['VT_INDEX_NAME']
})

VT_MEILI_URL = app.config.get('VT_MEILI_URL')
VT_INDEX_NAME = app.config.get('VT_INDEX_NAME')


app.blueprint(login)




# APIs

###############
# THE FOLLOWING APIs ARE FOR LEARNING PURPOSE.
###############

@app.get("/")
async def hello_api(request: Request):
    # First log the Request received
    vt_logger_.error(f'Hello World API serviced.')
    return text(f'Hello World API serviced. No API token needed.')


@app.post("/secure")
@protected
async def secure_api(request: Request):
    # First log the Request received
    vt_logger_.error(f'To go fast, you must be fast!')
    return text(f'To go fast, you must be fast!\n\r')

#
# Module APIs
#


@app.post("/user-context")
#protected
async def user_context(request: Request):
    """User Context
    summary="This API takes a keyword as input from the user and uses Meilisearch to retrieve context from database.",
  
    openapi:
    ---
    operationId: UserContext
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              query:
                type: string
            required:
              - query
    responses:
      '200':
        description: Success
        content:
          application/json:
            schema:
              type: object
              properties:
                context:
                  type: object
                  properties:
                    '@context':
                      type: string
                    '@type':
                      type: string
                    query:
                      type: string
                    entities:
                      type: object
                      properties:
                        entity1:
                          type: string
                        entity2:
                          type: string
                    metadata:
                      type: object
                      properties:
                        timestamp:
                          type: string
                          format: date-time
                        source:
                          type: string
      '400':
        description: Invalid input
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
      '500':
        description: Internal server error
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
    """
    try:
        vt_logger_.info('Received user context!')
        received_data =  request.json
        vt_logger_.error(received_data)
        text_input = received_data.get('text') if received_data else "No text received"
        vt_logger_.info(f'Text input: {text_input}')

        async with  httpx.AsyncClient() as client:
            search_response = await client.post(
                f'{VT_MEILI_URL}/indexes/{VT_INDEX_NAME}/search',
                json={"q": text_input}
            )
            search_results = search_response.json()
            vt_logger_.error(f'Search results: {search_results}')

        # Build local data context from MeiliSearch results
        local_data_context = {}
        if 'hits' in search_results:
            for hit in search_results['hits']:
                local_data_context[hit['id']] = {
                    "businessName": hit['businessName'],
                    "description": hit['description']
                }

            return json({"localDataContext": local_data_context})
    except Exception as e:
        vt_logger_.error(f'Error in user_context: {str(e)}')
        return json({'error': str(e)}, status=500)


@app.post("/user-context-multi-input")
#protected
async def fetch_user_contexts(request: Request):
    
    """
    User Context Multi Input

    This API takes an array of keywords as input from the user and uses Meilisearch to retrieve context from the database.

    openapi:
    ---
    operationId: User Context Multi Input
    parameters:
      - name: Keywords
        in: query
        description: An array of keywords (minimum 1)
        required: true
        schema:
          type: array
          format: string
    responses:
        '200':
            description: Success
            content:
                application/json:
                    schema:
                        type: array
                        items:
                            type: string
                    examples:
                        example1:
                            value: ["Document 1", "Document 2", "Document 3"]
                        example2:
                            value: ["Document 4", "Document 5"]
        '400':
            description: Bad Request
        '401':
            description: Unauthorized
        '500':
            description: Error
    """

    api_wrapper = UserContextAPIWrapper()
    received_data = request.json
    textList = received_data.get('text', ["No text received"])
    if not isinstance(textList, list):
        textList = ["No text received"]
    responseList = []
    responses = await api_wrapper.post_user_context(textList)
    for response in responses:
        if isinstance(response, Exception):
            vt_logger_.error(f'Error: {str(response)}')
            responseList.append({'error': str(response)})
        else:
            responseList.append(response.get("localDataContext", {}))
    return json({"responses": responseList})




# @app.post("/user-context-multi-threading")
# async def user_context_multi_threading(request: Request):
#     try:
#         vt_logger_.error(f'Created new thread')
#         thread = threading.Thread(target=user_context, args=(request,))
#         thread.start()
#         return json({"message": "API call initiated in a separate thread"})

#     except Exception as e:
#         return json({'error': str(e)}, status_code=500)

# def threading_test(secs):
#     vt_logger_.error(f'Waiting for {secs} seconds.')
#     time.sleep(int(secs))
#     vt_logger_.error(f'Finished waiting for {secs} seconds.')

# @app.post("/multi-threading-test")
# async def multi_threading_test(request: Request):
#     try:
#         vt_logger_.error(f'Created new thread')
#         received_data = request.json
#         vt_logger_.error(received_data)
#         text_input = received_data.get('text') if received_data else "No text received"
#         vt_logger_.error(f'Text input: {text_input}')
#         thread = threading.Thread(target=threading_test, args=(text_input,))
#         thread.start()
#         thread.join()
#         return json({"message": "API call initiated in a separate thread"})

#     except Exception as e:
#         return json({'error': str(e)}, status_code=500)



@app.route("/endpoint", methods=["POST"])
async def receive_message(request):
    message = request.json.get('message')
    name = request.json.get('name')
    vt_logger_.info(f"Received message: {message} by {name}")
    return json({'message':"message received"})

# Function to handle exiting threads gracefully   
def handle_exit(sig, frame):
    vt_logger_.info("Ctrl+C detected. Stopping threads...")
    stop_event.set()
    vt_logger_.info(f"Number of bot instances: {len(bot_instances)}")
    
    # Disconnect each bot
    for bot in bot_instances:
        vt_logger_.info(f'Disconnecting {bot.name}')
        bot.disconnect(wait=True)
        
    # Stop each event loop    
    for loop in bot_event_loops:
        loop.call_soon_threadsafe(loop.stop)
        
    vt_logger_.info("All threads have stopped.") 
    
    # Join each thread to ensure they have finished
    for thread in bot_threads:
            thread.join()
               
    sys.exit(0)  
    
# Worker function for the bot, runs in a separate thread.
def bot_worker(config):
    # Create a new event loop for the bot thread
    print("bot started")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Initialize the bot with the given configuration
    bot = VTXMPPAgent(config)
    
    # Connect the bot to the XMPP server
    bot.connect(use_ssl=False, force_starttls=False, disable_starttls=True)
    print("bot connected")
    
    # Store the bot and its event loop for later reference
    bot_instances.append(bot)   
    bot_event_loops.append(loop)
    print("bot added")

    try:
        # This keeps the loop running until the bot disconnects
        print("loop started")
        loop.run_until_complete(bot.disconnected)  
    except Exception as e:
        print("exception")
        vt_logger_.info(f"Error in bot process: {e}")
    finally:
       # Ensure all asynchronous generators are cleaned up
        pending = asyncio.all_tasks(loop)
        for task in pending:
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                loop.run_until_complete(task)
        loop.run_until_complete(loop.shutdown_asyncgens()) 
        loop.close() 
        print("loop completed")

if __name__ == "__main__":
    # Start a thread for each bot configuration
    for config in VT_AGENT_CONFIG:
        thread = threading.Thread(target=bot_worker, args=(config,))
        thread.start()
        bot_threads.append(thread)

    app.run(debug=False, access_log=False, fast=True)
