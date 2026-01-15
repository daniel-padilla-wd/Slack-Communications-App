"""
Modal handlers for opening and managing modals.
"""
from blocks import compose_modal_blocks


def register_modal_handlers(app):
    """Register all modal-related handlers."""
    
    @app.shortcut("bt_comms_shortcut")
    def open_modal(ack, body, client, logger, shortcut):
        # Acknowledge the shortcut request
        ack()
        # logger.info(body)
        modal_view = compose_modal_blocks()
        # Call the views_open method using the built-in WebClient
        client.views_open(
            trigger_id=shortcut["trigger_id"],
            # A simple view payload for a modal
            view={
                "title": {
                    "type": "plain_text",
                    "text": "BT Comms App",
                    "emoji": True
                },
                "submit": {
                    "type": "plain_text",
                    "text": "Submit",
                    "emoji": True
                },
                "type": "modal",
                "close": {
                    "type": "plain_text",
                    "text": "Cancel",
                    "emoji": True
                },
                "callback_id": "initial_view",
                "private_metadata": "",
                "blocks": modal_view
            }
        )
