import os
import logging
from dotenv import load_dotenv
load_dotenv()

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.web import WebClient

logging.basicConfig(level=logging.DEBUG)

import ssl
import certifi

# Import handler registration functions
from handlers import modal_handlers, checkbox_handlers, dropdown_handlers, input_handlers, submission_handlers

# Get the path to the certifi CA bundle
ca_file_path = certifi.where()

# Create a custom SSL context
context = ssl.create_default_context(cafile=ca_file_path)

# Disable the strict verification flag
context.verify_flags &= ~ssl.VERIFY_X509_STRICT

# Initialize the WebClient with the custom SSL context
# This client will be used by the Bolt app for all API calls.
client = WebClient(
    token=os.getenv("SLACK_BOT_TOKEN"),
    ssl=context
)

# Initialization
app = App(client=client)

# Register all handlers
modal_handlers.register_modal_handlers(app)
checkbox_handlers.register_checkbox_handlers(app, client)
dropdown_handlers.register_dropdown_handlers(app, client)
input_handlers.register_input_handlers(app)
submission_handlers.register_submission_handlers(app, client)

# Start Bolt app
if __name__ == "__main__":
    SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()
