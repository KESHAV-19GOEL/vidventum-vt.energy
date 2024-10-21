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

import sys
import asyncio
import threading
import contextlib
from sanic import Sanic
from sanic.response import json
from vt_auth.login import login
from vt_run.config.server_config import VT_SANIC_SETUP
from vt_agents.vt_XMPP_Agent import VTXMPPAgent
from vt_run.config.agent_config import agent_config 
from vt_logging.vt_botlogger_ import vt_botlogger_  

# Global variables to hold bot instances and event loops
bot_instances_G= []
bot_event_loops_G = []
bot_threads_G = []

# Dictionary to hold thread-specific context
Agent_thread_context_G = {}

# Create API Server App and initialize with config file.
app = Sanic(VT_SANIC_SETUP['VT_MODULE_NAME'])
app.update_config(VT_SANIC_SETUP['VT_SANIC_SERVER_CONFIG_FILE'])

# Register login blueprint
app.blueprint(login)

# Endpoint to receive messages from bots
@app.route("/send_message_to_resolution_layer", methods=["POST"])
async def send_message_to_resolution_layer(request):
    """
    Receives a message and logs it.

    This endpoint receives a JSON payload containing a message and a name,
    logs the information, and returns a confirmation response.

    Args:
        request (sanic.request.Request): The HTTP request object containing the JSON payload.

    JSON Parameters:
        message (str): The message sent to the bot.
        name (str): The name of the bot receiving the message.

    responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    description: A confirmation message indicating that the message was received.
        '400':
          description: Invalid input
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    description: Error message indicating the reason for invalid input.
        '500':
          description: Internal server error
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    description: Error message indicating an internal server error.
    """
    message = request.json.get('message')
    name = request.json.get('name')
    vt_botlogger_.info(f"Received message: {message} by {name}")
    return json({'message': "message received"})

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
    bot_instances_G.append(bot)   
    bot_event_loops_G.append(event_loop)

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
        
    vt_botlogger_.info(f"Number of bot instances: {len(bot_instances_G)}")
        
    # Stop each event loop    
    for loop in bot_event_loops_G:
        loop.run_in_executor(None, loop.stop) # this allocates a separate thread to stop the loop.
        
    vt_botlogger_.info("All threads have stopped.") 
    
    # Join each thread to ensure they have finished
    for thread in bot_threads_G:
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
            thread_id = len(bot_threads_G) + 1
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
            bot_threads_G.append(agent_thread)
            agent_thread.start()
            
    return bot_threads_G

if __name__ == "__main__":
    # Start Function for bot threads
    bot_threads_G = start_agents()
   
    try:
        app.run(debug=False, access_log=False, fast=True)
    finally:
        handle_exit()
        