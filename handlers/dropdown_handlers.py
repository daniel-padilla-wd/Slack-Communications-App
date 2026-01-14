"""
Dropdown action handlers for selecting number of CTA buttons.
"""
from blocks import compose_modal_blocks
from slack_sdk.errors import SlackApiError
import time


def register_dropdown_handlers(app, client):
    """Register all dropdown-related handlers."""
    
    @app.action("call_to_action_dropdown-action")
    def handle_call_to_action_dropdown_action(ack, body, logger):
        ack()
        logger.info(body)

        call_to_action_dropdown_selected = body["actions"][0]["selected_option"]
        call_to_action_requested_buttons = body["actions"][0]["selected_option"]["value"]
        customize_sender_identity_selected = bool(body["view"]["state"]["values"]["customize_sender_identity"]["customize_sender_identity-action"].get("selected_options", []))

        if call_to_action_dropdown_selected:
            if not customize_sender_identity_selected:
                logger.info("--------------------------------\n")
                logger.info("CUSTOMIZE SENDER ID unchecked.\n")
                logger.info(f"CALL TO ACTION DROPDOWN selected option: {call_to_action_dropdown_selected}\n")
                logger.info(f"REQUESTED NUMBER OF BUTTONS: {call_to_action_requested_buttons}\n")
                logger.info("Generating corresponding number of CTA button input fields...\n")
            else:
                logger.info("--------------------------------\n")
                logger.info(f"CALL TO ACTION DROPDOWN selected option: {call_to_action_dropdown_selected}\n")
                logger.info(f"REQUESTED NUMBER OF BUTTONS: {call_to_action_requested_buttons}\n")
                logger.info("Generating corresponding number of CTA button input fields...\n")
        
        blocks = compose_modal_blocks(
            include_sender_identity=customize_sender_identity_selected,
            include_cta_dropdown=True,
            num_cta_buttons=int(call_to_action_requested_buttons)
        )

        # Retry logic for hash conflicts in Lambda environment
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Get fresh view state on retries
                current_hash = body["view"]["hash"] if attempt == 0 else ""
                
                client.views_update(
                    view_id=body["view"]["id"],
                    hash=current_hash,
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
                break  # Success, exit retry loop
            except SlackApiError as e:
                if e.response["error"] == "hash_conflict" and attempt < max_retries - 1:
                    logger.warning(f"Hash conflict on attempt {attempt + 1}, retrying without hash...")
                    time.sleep(0.1 * (attempt + 1))  # Brief backoff
                else:
                    logger.error(f"Failed to update view: {e}")
                    raise
