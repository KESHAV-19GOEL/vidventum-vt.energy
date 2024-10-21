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
# import threading
# from abc import ABC, abstractmethod

# class VTBaseAgent(ABC, threading.Thread):
#     def __init__(self, config, logger):
#         super().__init__()
#         self.config = config
#         self.logger = logger
#         self.name = config.get('Name', 'UnnamedAgent')
#         self.uid = config.get('UID', 'UnknownUID')
#         self.description = config.get('Description', 'No description provided')
#         self.type = config.get('Type', 'UnknownType')

#     @abstractmethod
#     async def connect(self):
#         """
#         Abstract method to establish connection.
#         Must be implemented by derived classes.
#         """
#         pass

#     @abstractmethod
#     async def disconnect(self):
#         """
#         Abstract method to disconnect.
#         Must be implemented by derived classes.
#         """
#         pass

#     @abstractmethod
#     async def process(self):
#         """
#         Abstract method to process agent-specific tasks.
#         Must be implemented by derived classes.
#         """
#         pass

#     async def run_agent(self):
#         """
#         Main coroutine method.
#         """
#         self.logger.info(f"Starting agent: {self.name}")
#         await self.connect()
#         try:
#             while True:
#                 await self.process()
#         except Exception as e:
#             self.logger.error(f"Error in agent {self.name}: {str(e)}")
#         finally:
#             await self.disconnect()
#             self.logger.info(f"Agent {self.name} stopped")

#     def run(self):
#         """
#         Main thread method.
#         """
#         import asyncio
#         asyncio.run(self.run_agent())