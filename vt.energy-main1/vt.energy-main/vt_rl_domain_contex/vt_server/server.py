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
import asyncio
import requests
import json as json_lib
import threading
import contextlib

import nats
from sanic import Sanic
from sanic.response import text, json
from sanic.request import Request
from sanic_ext import Extend, openapi

from vt_logging.vt_botlogger_ import vt_botlogger_  
from vt_auth.auth import protected
from vt_auth.login import login
from vt_api_handlers.languages.google import translate_text
from vt_run.config.server_config import VT_SANIC_SETUP, VT_MEILI_SETUP
from vt_run.config.agent_config import agent_config 
from vt_agents.vt_xmpp_agent import VTXMPPAgent

# Global variables to hold bot instances and event loops
bot_instances = []
bot_event_loops = []
bot_threads = []

# Dictionary to hold thread-specific context
Agent_thread_context_G = {}

# Create API Server App and initialize with config file.
app = Sanic(VT_SANIC_SETUP['VT_MODULE_NAME'])#, request_class=VtNanoSecondRequest)
app.update_config(VT_SANIC_SETUP['VT_SANIC_SERVER_CONFIG_FILE'])

# Initialize MeiliSearch configuration globally
index_name = VT_MEILI_SETUP['VT_INDEX_NAME']
base_url = VT_MEILI_SETUP['VT_BASE_URL']
search_url = f'{base_url}/indexes/{index_name}/search'

app.blueprint(login)

# Register the OpenAPI extension with metadata
# app.config.API_TITLE = "Business Context API"
# app.config.API_DESCRIPTION = "This API accepts a user context, queries the documents using Meilisearch, and returns the corresponding business context based on the provided query."
# app.config.API_VERSION = "1.0.0"

# Extend(app)

# APIs

###############
# THE FOLLOWING APIs IMPLEMENT THE MODULE FUNCTIONALITY. 
###############

@app.post("/get-business-context")
@openapi.definition(
    summary="Fetch business context data based on user context from MeiliSearch",
    description="This API accepts a user context, queries the documents using Meilisearch, and returns the corresponding business context based on the provided query.",
    tag="business context"
)
@openapi.body(
    {"application/json": openapi.Schema(
        type="object",
        properties={"user_context": openapi.Schema(type="string")},
        required=["user_context"]
    )}
)
@openapi.response(
    200,
    {"application/json": openapi.Schema(
        type="object",
        properties={
            "context": openapi.Schema(
                type="object",
                properties={
                    "@context": openapi.Schema(type="string"),
                    "@type": openapi.Schema(type="string"),
                    "query": openapi.Schema(type="string"),
                    "business-context": openapi.Schema(type="string"),
                    "metadata": openapi.Schema(
                        type="object",
                        properties={
                            "timestamp": openapi.Schema(type="string", format="date-time"),
                            "source": openapi.Schema(type="string")
                        }
                    )
                }
            )
        }
    )}
)
@openapi.response(
    400,
    {"application/json": openapi.Schema(
        type="object",
        properties={"error": openapi.Schema(type="string")}
    )}
)
@openapi.response(
    500,
    {"application/json": openapi.Schema(
        type="object",
        properties={"error": openapi.Schema(type="string")}
    )}
)
async def get_business_context(request: Request):
    """

    """
    user_context = request.json.get('user_context')
    if not user_context:
        return json({"error": "Missing or invalid user context."}, status=400)

    search_params = {"q": user_context}

    vt_botlogger_.info(f'Search URL: {search_url}')
    vt_botlogger_.info(f'Search Params: {search_params}')
    
    try:
        response = requests.post(search_url, json=search_params)
        
        if response.status_code == 200:
            business_data = response.json()
            result = ' '.join(map(lambda x: x['businessName'], business_data['hits']))
            return json({"context": {
                "@context": "https://schema.org",
                "@type": "BusinessContext",
                "query": user_context,
                "business-context": result,
                "metadata": {
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "source": "api"
                }
            }})
        
        else:
            vt_botlogger_.error(f"MeiliSearch returned an error: {response.status_code} {response.text}")
            return json({"error": "Failed to fetch business data from MeiliSearch"}, status=500)
        
    except Exception as e:
        vt_botlogger_.error(f"Error fetching business data: {str(e)}")
        return json({"error": "An error occurred while fetching business data"}, status=500)
    
# Worker function for the bot, runs in a separate thread.
def bot_worker(config, thread_context,logger):
    """
    Worker function to run a bot in a separate thread.

    This function initializes a VTXMPPAgent bot, connects it to the XMPP server, 
    and keeps it running until the stop event is set or the bot disconnects.

    Args:
        config (dict): The configuration for the bot.
        thread_context (dict): The context for the thread, containing:
            - thread_id (int): The ID of the thread.
            - loop (asyncio.AbstractEventLoop): The event loop for the thread.
            - stop_event (threading.Event): The event to signal the thread to stop.
        logger: logger for the bot.    

    Raises:
        Exception: If an error occurs during the bot process, it logs the error message.

    """
    # Unpack thread context
    agent_thread_id = thread_context['thread_id']
    event_loop = thread_context['loop']
    agent_stop_event = thread_context['stop_event']

    asyncio.set_event_loop(event_loop)

    # Initialize the bot with the given configuration
    bot = VTXMPPAgent(config, logger)
    
    # Connect the bot to the XMPP server
    bot.connect(use_ssl=False, force_starttls=False, disable_starttls=True)
    
    # Store the bot and its event loop for later reference
    bot_instances.append(bot)   
    bot_event_loops.append(event_loop)

    try:
        # This keeps the loop running until the bot disconnects or stop event is set
        while not agent_stop_event.is_set():
            event_loop.run_until_complete(bot.disconnected)
    except Exception as e:
        logger.error(f"Error in bot process: {e}")
    finally:
        # Disconnect the bot
        logger.info(f'Disconnecting {bot.name}')
        bot.disconnect(wait=True)  
        # Ensure all asynchronous generators are cleaned up
        pending = asyncio.all_tasks(event_loop)
        for task in pending:
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                event_loop.run_until_complete(task)
        event_loop.run_until_complete(event_loop.shutdown_asyncgens()) 
        event_loop.close() 
        
# Function to handle exiting threads gracefully   
def handle_exit():
    """
    Gracefully handles the exit process for all bot threads.

    This function is triggered when a signal (such as Ctrl+C) is detected. It sets
    the stop_event to signal all threads to stop, disconnects each bot, stops each 
    event loop, and joins all threads to ensure they have finished before exiting 
    the program.
  
    Logs:
        Information about the number of bot instances and the disconnection process.
    """ 
    vt_botlogger_.info("Ctrl+C detected. Stopping threads...")
    # Set stop event for each thread
    for context in Agent_thread_context_G.values():
        context['stop_event'].set()
        
    vt_botlogger_.info(f"Number of bot instances: {len(bot_instances)}")
        
    # Stop each event loop    
    for loop in bot_event_loops:
        loop.run_in_executor(None, loop.stop) # this allocates a separate thread to stop the loop.
        
    vt_botlogger_.info("All threads have stopped.") 
    
    # Join each thread to ensure they have finished
    for thread in bot_threads:
        thread.join()
               
    sys.exit(0)    

# Start a thread for each bot configuration
def start_agents():
    """
    Starts a thread for each bot configuration.

    This function iterates through the agent configurations, creates a thread context
    for each bot, and starts a new thread running the bot_worker function with the 
    appropriate configuration and thread context.

    Returns:
        list: A list of all the bot threads that were started.
    """
    for config in agent_config:
        if config['Type'] == 'VT_XMPP_AGENT':
            # Create thread context
            thread_id = len(bot_threads) + 1
            loop = asyncio.new_event_loop()
            stop_event = threading.Event()
            thread_context = {
                'thread_id': thread_id,
                'loop': loop,
                'stop_event': stop_event
            }
            Agent_thread_context_G[thread_id] = thread_context
            
            # Start the thread
            agent_thread = threading.Thread(target=bot_worker, args=(config, thread_context, vt_botlogger_))
            agent_thread.daemon = True  # Daemonize the thread
            bot_threads.append(agent_thread)
            agent_thread.start()
            
    return bot_threads

if __name__ == "__main__":
    # Start Function for bot threads
    bot_threads = start_agents()
   
    try:
        app.run(debug=False, access_log=False, fast=True)
    finally:
        handle_exit()
        