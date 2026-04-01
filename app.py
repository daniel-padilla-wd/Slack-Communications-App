"""Bootstrap and start the Slack Bolt application."""

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.web import WebClient

# Import configuration
from config import Config, BOT_TOKEN, SIGNING_SECRET, APP_TOKEN, SSL_CONTEXT

# Import handler registration functions
from handlers import modal_handlers, checkbox_handlers, dropdown_handlers, input_handlers, submission_handlers

# Setup logging
Config.setup_logging()

# Initialize Slack Bolt app
app = App(
    signing_secret=SIGNING_SECRET,
    process_before_response=True,
    client=WebClient(token=BOT_TOKEN, ssl=SSL_CONTEXT)
)

# Register all handlers
modal_handlers.register_modal_handlers(app)
checkbox_handlers.register_checkbox_handlers(app)
dropdown_handlers.register_dropdown_handlers(app)
input_handlers.register_input_handlers(app)
submission_handlers.register_submission_handlers(app)

# Start Bolt app (local development with Socket Mode)
if __name__ == "__main__":
    SocketModeHandler(app, APP_TOKEN).start()
