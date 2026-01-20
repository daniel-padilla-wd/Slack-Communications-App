"""
Modal handlers for opening and managing modals.
"""
from blocks import compose_modal_blocks


def register_modal_handlers(app):
    """Register all modal-related handlers."""
    
    @app.shortcut("bt_comms_shortcut")
    def open_modal(ack, body, client, logger, shortcut):
        ack()
        modal_view = compose_modal_blocks()
        client.views_open(
            trigger_id=shortcut["trigger_id"],
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
