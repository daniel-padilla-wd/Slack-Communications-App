"""
View submission handlers for processing modal submissions.
"""
import logging
from services import generate_cta_button_elements, customize_sender_identity_state, send_message_to_conversation


def register_submission_handlers(app, client):
    """Register all submission-related handlers."""
    
    @app.view("initial_view")
    def handle_comms_submission_event(ack, body, logger, view):
        logger.info(body)
        rich_text_input_value: str = view["state"]["values"]["rich_text_input"]["rich_text_input-action"]["rich_text_value"]

        try:
            # Validate conversation_select_block
            multi_conversations_selected: list = view["state"]["values"]["conversation_select_block"]["conversation_select_action"]["selected_conversations"]
            if not multi_conversations_selected:
                logging.info("\nNO CONVERSATIONS SELECTED\n")
                ack(response_action="errors", errors={
                    "conversation_select_block": "Please select at least one conversation to send the message to."
                })
                return
            
            # Validate CTA button links
            import validators
            number_of_buttons_selected: int = int(view["state"]["values"]["call_to_action_dropdown"]["call_to_action_dropdown-action"]["selected_option"]["value"])
            logger.info(f"\nNUMBER OF BUTTONS SELECTED: {number_of_buttons_selected}\n")
            for i in range(number_of_buttons_selected):
                button_link_value = view["state"]["values"][f"cta_button_link_{i+1}"]["cta_button_link_input-action"]["value"].strip()
                logging.info(f"\nVALIDATING BUTTON LINK {i+1}: {button_link_value}\n")
                logging.info(f"\nSTARTS WITH HTTP: {button_link_value.startswith('http://')}\n")
                logging.info(f"\nSTARTS WITH HTTPS: {button_link_value.startswith('https://')}\n")
                if validators.url(button_link_value):
                    pass
                else:
                    # If validation fails, return an error payload
                    logging.info(f"\nINVALID URL DETECTED FOR BUTTON LINK {i+1}: {button_link_value}\n")
                    ack(response_action="errors", errors={
                        f"cta_button_link_{i+1}": "Please enter a valid URL that starts with http:// or https://"
                    })
                    return
            ack()
            buttons = generate_cta_button_elements(view, number_of_buttons_selected, logger)
        except Exception as e:
            logging.warning(f"\n Exception occurred: {e}\n")
            ack()
            buttons = None
        
        # Main Logic
        sender_identity = customize_sender_identity_state(view)
        if sender_identity is not None:
            for conversation_id in multi_conversations_selected:
                send_message_to_conversation(
                    client=client,
                    conversation_id=conversation_id,
                    blocks=[rich_text_input_value],
                    logger=logger,
                    sender_name=sender_identity["sender_name"],
                    icon_url=sender_identity["icon_url"],
                    cta_elements=buttons
                )
        else:
            for conversation_id in multi_conversations_selected:
                send_message_to_conversation(
                    client=client,
                    conversation_id=conversation_id,
                    blocks=[rich_text_input_value],
                    logger=logger,
                    cta_elements=buttons
                )
