"""
Business logic services for message processing and CTA handling.
"""
from slack_sdk.errors import SlackApiError

def generate_cta_button_elements(view, number_of_buttons, logger):
    """
    Generate CTA button elements from view state.
    
    Args:
        view: The view object containing state values
        number_of_buttons: Number of buttons to generate
        logger: Logger instance for debugging
    
    Returns:
        List of button block elements or None if error occurs
    """
    try:
        elements = []
        for i in range(number_of_buttons):
            button_text = view["state"]["values"][f"cta_button_text_{i+1}"]["cta_button_text_input-action"]["value"]
            button_link = view["state"]["values"][f"cta_button_link_{i+1}"]["cta_button_link_input-action"]["value"].strip()
            button = {
                "type": "actions",
                "block_id": f"button_id_{i+1}",
                "elements": [
                    {
                        "type": "button",
                        "action_id": f"button_action_{i+1}",
                        "text": {
                            "type": "plain_text",
                            "text": button_text,
                            "emoji": True
                        },
                        "url": button_link
                    }
                ]
            }
            elements.append(button)
        # logger.info(f"\nHere are the generated CTA elements: {elements}\n")
        return elements
    except Exception as e:
        logger.error(f"Error generating CTA button elements: {e}")
        return None


def customize_sender_identity_state(view):
    """
    Extract sender identity information from view state.
    
    Args:
        view: The view object containing state values
    
    Returns:
        Dict with sender_name and icon_url or None if not selected
    """
    customize_sender_identity_selected = view["state"]["values"]["customize_sender_identity"]["customize_sender_identity-action"].get("selected_options")
    if customize_sender_identity_selected:
        try:
            sender_name_value = view["state"]["values"].get("sender_name").get("sender_name_input-action").get("value")
        except:
            sender_name_value = None
        try:
            icon_url_value = view["state"]["values"].get("icon_url").get("icon_url_input-action").get("value")
        except:
            icon_url_value = None
        return {"sender_name": sender_name_value, "icon_url": icon_url_value}
    return None


def send_message_to_conversation(client, conversation_id, blocks, logger, caller_user_id, sender_name=None, icon_url=None, cta_elements=None):
    """
    Send a message to a Slack conversation.
    
    Args:
        client: Slack WebClient instance
        conversation_id: ID of the conversation to send to
        blocks: Message blocks to send
        logger: Logger instance
        caller_user_id: user.id of the user who invoked the shortcut
        sender_name: Optional custom sender name
        icon_url: Optional custom icon URL
        cta_elements: Optional list of CTA button elements
    """
    notification_text = "Message from Slack Communications App"
    message_payload = {
        "channel": conversation_id,
        "text": notification_text,
        "blocks": blocks
    }
    if sender_name:
        message_payload["username"] = sender_name
    if icon_url:
        message_payload["icon_url"] = icon_url
    if cta_elements:
        # logger.info(f"\nCTA ELEMENTS TO BE ADDED: {cta_elements}\n")
        message_payload["blocks"] = [*blocks, *cta_elements]

    # logger.info(f"\nMESSAGE PAYLOAD TO BE SENT: {message_payload}\n")
    try:
        client.chat_postMessage(**message_payload)
    except SlackApiError as e:
        logger.error(f"Error sending message to conversation {conversation_id}: {e}")
        client.chat_postMessage(
            channel=caller_user_id,
            text=f":warning: Failed to send message to <#{conversation_id}>. Ensure that the app is added to the channel's workspace and is approved for the workspace, or if the channel is private, add the app to the channel.\n Error details for INC: {e.response['error']}"
        )
        return
