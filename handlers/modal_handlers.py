"""
Modal handlers for opening and managing modals.
"""
from blocks import compose_modal_blocks
from config import Config


def register_modal_handlers(app):
    """Register all modal-related handlers."""

    allowed_user_ids = set(Config.ALLOWED_SHORTCUT_USER_IDS)

    def authorize_shortcut_user(ack, body, client, logger, next):
        if not Config.PRODUCTION:
            next()
            return

        user_payload = body.get("user", {})
        user_id = user_payload.get("id")

        if user_id in allowed_user_ids:
            next()
            return
        ack()

        trigger_id = body.get("trigger_id")
        if not trigger_id:
            logger.warning("Unauthorized shortcut access for user_id=%s (no trigger_id)", user_id)
            return

        client.views_open(
            trigger_id=trigger_id,
            view={
                "type": "modal",
                "callback_id": "unauthorized_access",
                "title": {
                    "type": "plain_text",
                    "text": "Access denied",
                    "emoji": True
                },
                "close": {
                    "type": "plain_text",
                    "text": "Close"
                },
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "\n:no_entry: You are not authorized to use this shortcut."
                        }
                    }
                ]
            }
        )
        logger.warning("Unauthorized shortcut access for user_id=%s", user_id)

    
    @app.shortcut("bt_comms_shortcut", middleware=[authorize_shortcut_user])
    def open_modal(ack, body, client, logger, shortcut):
        ack()
        logger.info(f"Payload recieved:\n{body}")
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
