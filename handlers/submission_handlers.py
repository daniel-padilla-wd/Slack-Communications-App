"""
View submission handlers for processing modal submissions.
"""
import validators
import logging
from services import generate_cta_button_elements, customize_sender_identity_state, send_message_to_conversation

def validate_icon_url(ack, view_state: dict) -> bool:
    logging.info(f"Validating icon URL with view state:\n{view_state}")
    try:
        if not view_state.get("icon_url"):
            return True  # No URL provided, so no validation needed
        if not view_state["icon_url"]["icon_url-action"].get("value"):
            return True  # No URL provided, so no validation needed
        icon_url_value: str = view_state["icon_url"]["icon_url-action"]["value"].strip()
        if not validators.url(icon_url_value):
            # If validation fails, return an error payload
            ack(response_action="errors", errors={
                f"icon_url": "Please enter a valid URL that starts with http:// or https://"
            })
            return False
    except Exception as e:
        logging.warning(f"\n Exception occurred during icon URL validation: {e}\n")
        return False
    return True

def validate_cta_button_links(ack, view_state: dict) -> bool:
    try: 
        if not view_state.get("call_to_action"):
            return True  # No CTA buttons selected, so no validation needed
        if not view_state["call_to_action"]["call_to_action-action"].get("selected_options"):
            return True  # No CTA buttons selected, so no validation needed
        if not view_state["call_to_action_dropdown"]["call_to_action_dropdown-action"].get("selected_option"):
            ack(response_action="errors", errors={
                "conversation_select_block": "Call to action is selected. Please select at least one call to action button."
            })
            return
        
        number_of_buttons_selected: int = len(view_state["call_to_action_dropdown"]["call_to_action_dropdown-action"]["selected_option"]["value"])
        for i in range(number_of_buttons_selected):
            button_link_value = view_state[f"cta_button_link_{i+1}"]["cta_button_link_input-action"]["value"].strip()
            if not validators.url(button_link_value):
                # If validation fails, return an error payload
                ack(response_action="errors", errors={
                    f"cta_button_link_{i+1}": "Please enter a valid URL that starts with http:// or https://"
                })
                return
    except Exception as e:
        logging.warning(f"\n Exception occurred during CTA button link validation: {e}\n")
        return False
    return True
    


def register_submission_handlers(app):
    """Register all submission-related handlers."""
    
    @app.view("initial_view")
    def handle_comms_submission_event(ack, body, client, logger, view):
        logger.info(f"Payload recieved:\n{body}")
        # rich_text_input_value: str = view["state"]["values"]["rich_text_input"]["rich_text_input-action"]["rich_text_value"]
        try:
            # Validate conversation_select_block
            multi_conversations_selected: list = view["state"]["values"]["conversation_select_block"]["conversation_select_action"]["selected_conversations"]
            if not multi_conversations_selected:
                ack(response_action="errors", errors={
                    "conversation_select_block": "Please select at least one conversation to send the message to."
                })
                return
            
            # Valid user icon url 
            if not validate_icon_url(ack, view["state"]["values"]):
                return
            
            # Validate CTA button links
            if not validate_cta_button_links(ack, view["state"]["values"]):
                return
            ack()
            #number_of_buttons_selected: int = int(view["state"]["values"]["call_to_action_dropdown"]["call_to_action_dropdown-action"]["selected_option"]["value"])
            #buttons = generate_cta_button_elements(view, number_of_buttons_selected, logger)
        except Exception as e:
            logging.warning(f"\n Exception occurred within handle_comms_submission_event: {e}\n")
            ack()
            buttons = None

       
        number_of_buttons_selected: int = int(view["state"]["values"]["call_to_action_dropdown"]["call_to_action_dropdown-action"]["selected_option"]["value"])
        buttons = generate_cta_button_elements(view, number_of_buttons_selected, logger)
        

        
        # Main Logic
        #logging.info(f"====These are the buttons:====\n Number of buttons {number_of_buttons_selected} \n{buttons}")
        rich_text_input_value: str = view["state"]["values"]["rich_text_input"]["rich_text_input-action"]["rich_text_value"]
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
