"""
Checkbox action handlers for sender identity and call-to-action options.
"""
from blocks import compose_modal_blocks


def register_checkbox_handlers(app, client):
    """Register all checkbox-related handlers."""
    
    @app.action("customize_sender_identity-action")
    def handle_customize_sender_id_checkbox(ack, body, logger):
        ack()
        # logger.info(body)
        
        customize_sender_identity_selected = bool(body["actions"][0]["selected_options"])
        call_to_action_selected = bool(body["view"]["state"]["values"]["call_to_action"]["call_to_action-action"].get("selected_options", []))
        
        call_to_action_buttons_selected = body["view"]["state"]["values"].get("call_to_action_dropdown", None)
        num_cta_buttons = 0

        # logger.info("--------------------------------\n")
        if customize_sender_identity_selected:
            # logger.info(f"\n customize_sender_identity_selected: {customize_sender_identity_selected}\n")
            # logger.info("\nCONDITIONAL CHECKS FOR CUSTOMIZE SENDER ID SELECTED\n")
            # logger.info("customize_sender_identity checked.\n")
            if call_to_action_buttons_selected:
                # logger.info("CTA BUTTONS TOGGLE DETECTED\n")
                try:
                    number_of_cta_buttons = body["view"]["state"]["values"].get("call_to_action_dropdown").get("call_to_action_dropdown-action").get("selected_option").get("value", None)
                    # logger.info(f"\nNUMBER OF CTA BUTTONS: {number_of_cta_buttons}\n")
                    num_cta_buttons = int(number_of_cta_buttons)
                except:
                    pass
        elif call_to_action_selected:
            # logger.info("\nCONDITIONAL CHECKS FOR CALL TO ACTION SELECTED\n")
            # logger.info("call_to_action checked.\n")
            if call_to_action_buttons_selected:
                # logger.info("CTA BUTTONS TOGGLE DETECTED\n")
                try:
                    number_of_cta_buttons = body["view"]["state"]["values"].get("call_to_action_dropdown").get("call_to_action_dropdown-action").get("selected_option").get("value", None)
                    # logger.info(f"\nNUMBER OF CTA BUTTONS: {number_of_cta_buttons}\n")
                    num_cta_buttons = int(number_of_cta_buttons)
                except:
                    pass
        # logger.info("--------------------------------\n")
        
        blocks = compose_modal_blocks(
            include_sender_identity=customize_sender_identity_selected,
            include_cta_dropdown=call_to_action_selected,
            num_cta_buttons=num_cta_buttons
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

    @app.action("call_to_action-action")
    def handle_call_to_action_checkbox(ack, body, logger):
        ack()
        # logger.info(body)
        
        call_to_action_selected = bool(body["actions"][0]["selected_options"])
        customize_sender_identity_selected = bool(body["view"]["state"]["values"]["customize_sender_identity"]["customize_sender_identity-action"].get("selected_options", []))
        
        blocks = compose_modal_blocks(
            include_sender_identity=customize_sender_identity_selected,
            include_cta_dropdown=call_to_action_selected
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
