"""
Dropdown action handlers for selecting number of CTA buttons.
"""
from blocks import compose_modal_blocks


def register_dropdown_handlers(app):
    """Register all dropdown-related handlers."""
    
    @app.action("call_to_action_dropdown-action")
    def handle_call_to_action_dropdown_action(ack, client, body, logger):
        """Update modal blocks based on selected CTA button count."""
        ack()
        logger.info(f"Payload recieved:\n{body}")
        # call_to_action_dropdown_selected = body["actions"][0]["selected_option"]
        call_to_action_requested_buttons = body["actions"][0]["selected_option"]["value"]
        customize_sender_identity_selected = bool(body["view"]["state"]["values"]["customize_sender_identity"]["customize_sender_identity-action"].get("selected_options", []))
        
        blocks = compose_modal_blocks(
            include_sender_identity=customize_sender_identity_selected,
            include_cta_dropdown=True,
            num_cta_buttons=int(call_to_action_requested_buttons)
        )

        client.views_update(
            view_id=body["view"]["id"],
            hash=body["view"]["hash"],
            view={
                "private_metadata": "",
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
                "blocks": blocks
            }
        )
