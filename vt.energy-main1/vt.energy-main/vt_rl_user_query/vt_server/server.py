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
import asyncio
import nats
import contextlib
import threading
import sys
from sanic import Sanic
from sanic.response import text, json
from sanic.request import Request
from sanic.exceptions import SanicException
from vt_basics.custom_requests import VtNanoSecondRequest
from vt_logging.config import vt_logger_
from vt_auth.auth import protected
from vt_auth.login import login
from vt_api_handlers.languages.google import translate_text
from vt_run.config.server_config import VT_SANIC_SETUP
from vt_run.config.agent_config import AGENT_CONFIG
from vt_agents.xmpp_agent import VTXMPPAgent
from dotenv import load_dotenv


#ENV Variables
load_dotenv()
for agent in AGENT_CONFIG['agents']:
    pwd_env = agent['VT_XMPP_CONN_OBJECT']['Password_Env']
    if os.getenv(pwd_env):
        print(f"Password for {agent['Name']} is set")
    else:
        print(f"Password for {agent['Name']} is NOT set")

# Create API Server App and initialize with config file.
app = Sanic(VT_SANIC_SETUP['VT_MODULE_NAME'], request_class=VtNanoSecondRequest)
app.update_config(VT_SANIC_SETUP['VT_SANIC_SERVER_CONFIG_FILE'])

app.blueprint(login)

# Global variables to hold bot instances and event loops
bot_instances = []
bot_event_loops = []
bot_threads = []
# Event to signal threads to stop
stop_event = threading.Event()


# APIs

###############
# THE FOLLOWING APIs ARE FOR LEEARNING PURPOSE.
###############

@app.get("/")
async def hello_api(request: Request):
    # First log the Request received
    vt_logger_.error(f'Hello World API serviced.')
    return text(f'Hello World API serviced. No API token needed.')


###############
# THE FOLLOWING APIs IMPLEMENT THE MODULE FUNCTIONALITY. 
###############

#
# Module APIs
#

# Function to generate random context (placeholder)

def generate_random_context(query):
    return {
        "@context": "https://schema.org",
        "@type": "UserContext",
        "query": query,
        "entities": {
            "entity1": "random_value1",
            "entity2": "random_value2"
        },
        "metadata": {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "source": "api"
        }
    }

# API endpoint to get user context
@app.post("/user-context")
@protected
async def get_user_context(request: Request):

  #The following docstring is for the documentation.
    """User Context

    This API takes a query from the user, calls the context generating function, and then returns the context of the query.

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
        query = request.json.get("query")
        if not query:
            raise SanicException("Query is required", status_code=400)
        
        context = generate_random_context(query)
        return json({"context": context})
    except Exception as e:
        vt_logger_.error(f"Error processing user context: {str(e)}")
        return json({"error": str(e)}, status=500)


###############
# FUNCTION FOR MULTIAGENT USING MULTITHREADING
###############
# Add a dictionary to hold thread-specific context
vt_thread_context = {}

# Update the bot_worker function
def bot_worker(config):
    thread_id = threading.get_ident()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Create thread context
    stop_event = threading.Event()
    thread_context = {
        'thread_id': thread_id,
        'loop': loop,
        'stop_event': stop_event
    }
    vt_thread_context[thread_id] = thread_context

    try:
        bot = VTXMPPAgent(config, vt_logger_)
        bot.connect(use_ssl=False, force_starttls=False, disable_starttls=True)
        
        bot_instances.append(bot)
        bot_event_loops.append(loop)
        
        while not stop_event.is_set():
            loop.run_until_complete(bot.disconnected)
    except Exception as e:
        vt_logger_.error(f"Error in bot worker for {config['Name']}: {e}")
    finally:
        # Clean up asynchronous generators
        pending = asyncio.all_tasks(loop)
        for task in pending:
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                loop.run_until_complete(task)
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()

# Update the handle_exit function
def handle_exit(sig, frame):
    vt_logger_.info("Ctrl+C detected. Stopping threads...")
    
    # Set stop event for each thread
    for context in vt_thread_context.values():
        context['stop_event'].set()
    
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

# Add a new endpoint to receive messages from bots
@app.route("/receive_message", methods=["POST"])
async def receive_message(request):
    message = request.json.get('message')
    name = request.json.get('name')
    vt_logger_.info(f"Received message: {message} by {name}")
    return json({'message': "message received"})

# Update the start_agents function
def start_agents():
    for config in AGENT_CONFIG['agents']:
        if config['Type'] == 'VT_XMPP_AGENT':
            thread = threading.Thread(target=bot_worker, args=(config,))
            thread.daemon = True
            bot_threads.append(thread)
            thread.start()
    return bot_threads

if __name__ == "__main__":
    try:
        bot_threads = start_agents()
        app.run(debug=False, access_log=False, fast=True)
    finally:
        if KeyboardInterrupt:
            handle_exit(None, None)