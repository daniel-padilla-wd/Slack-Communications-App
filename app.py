from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
from slack_sdk.web import WebClient
#import logging
#logging.basicConfig(level=logging.INFO)

# Import configuration
from config import Config, BOT_TOKEN, SIGNING_SECRET, APP_TOKEN, SSL_CONTEXT

# Import handler registration functions
from handlers import modal_handlers, checkbox_handlers, dropdown_handlers, input_handlers, submission_handlers

# Setup logging
Config.setup_logging()

# Validate configuration
Config.validate()

# Initialize the WebClient with the custom SSL context
client = WebClient(token=BOT_TOKEN, ssl=SSL_CONTEXT)

# Initialize Slack Bolt app
# Signing secret only needed for Lambda/production (HTTP mode), not Socket Mode
if not Config.PRODUCTION:
    app = App(client=client)
else:
    app = App(client=client, signing_secret=SIGNING_SECRET)

# Register all handlers
app.client.auth_test()  # Test authentication
#modal_handlers.register_modal_handlers(app)
#checkbox_handlers.register_checkbox_handlers(app, client)
#dropdown_handlers.register_dropdown_handlers(app, client)
#input_handlers.register_input_handlers(app)
#submission_handlers.register_submission_handlers(app, client)

def lambda_handler(event, context):
    """
    AWS Lambda handler for Slack events.
    
    Args:
        event: AWS Lambda event object containing Slack request
        context: AWS Lambda context object
        
    Returns:
        Response dict with statusCode and body
    """
    #SlackRequestHandler.clear_all_log_handlers()
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)

# Start Bolt app (local development with Socket Mode)
if __name__ == "__main__":
    SocketModeHandler(app, APP_TOKEN).start()
