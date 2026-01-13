import os
import logging
from dotenv import load_dotenv
load_dotenv()

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.web import WebClient

logging.basicConfig(level=logging.DEBUG)

import ssl
import certifi

# Get the path to the certifi CA bundle
ca_file_path = certifi.where()

# Create a custom SSL context
context = ssl.create_default_context(cafile=ca_file_path)

# Disable the strict verification flag
context.verify_flags &= ~ssl.VERIFY_X509_STRICT

# Initialize the WebClient with the custom SSL context
# This client will be used by the Bolt app for all API calls.
client = WebClient(
    token=os.getenv("SLACK_BOT_TOKEN"),
    ssl=context
)

# Initialization
app = App(client=client)

initial_view_blocks = [
    {
        "type": "input",
        "element": {
            "type": "rich_text_input",
            "action_id": "rich_text_input-action"
        },
        "block_id": "rich_text_input",
        "label": {
            "type": "plain_text",
            "text": "Message",
            "emoji": True
        }
    },
    # Gemini provided the conversations select block below. This was not avalilable in Block Kit Builder.
    {
        "type": "input",
        "block_id": "conversation_select_block",
        "label": {
            "type": "plain_text",
            "text": "Choose a conversation:"
        },
        "element": {
            "type": "multi_conversations_select",
            "placeholder": {
                "type": "plain_text",
                "text": "Select a conversation"
            },
            "action_id": "conversation_select_action"
        }
    },
    {
        "type": "divider",
        "block_id": "divider_1"
    }
]

advanced_options_blocks = [
    {
        "type": "actions",
        "block_id": "customize_sender_identity",
        "elements": [
            {
                "type": "checkboxes",
                "options": [
                    {
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Do you need to customize the sender identity?*"
                        },
                        "description": {
                            "type": "plain_text",
                            "text": "I want to specify a custom sender name and a custom icon for my message, so that I can align the message's persona with its content.",
                            "emoji": True
                        },
                        "value": "value-0"
                    }
                ],
                "action_id": "customize_sender_identity-action"
            }
        ]
    },
    {
        "type": "actions",
        "block_id": "call_to_action",
        "elements": [
            {
                "type": "checkboxes",
                "options": [
                    {
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Do you need add in-context call to action?*"
                        },
                        "description": {
                            "type": "plain_text",
                            "text": "I want to add one or more clickable buttons with external links to my message, so that I can guide users to take a specific, immediate action.",
                            "emoji": True
                        },
                        "value": "value-1"
                    }
                ],
                "action_id": "call_to_action-action"
            }
        ]
    }
]

sender_identity_fields = [
    {
        "type": "divider",
        "block_id": "start_sender_identity_fields"
    },
    {
        "type": "input",
        "block_id": "sender_name",
        "element": {
            "type": "plain_text_input",
            "action_id": "plain_text_input-action",
            "placeholder": {
                "type": "plain_text",
                "text": "If left blank, the default name is used."
            }
        },
        "hint": {
            "type": "plain_text",
            "text": "A Slack bot's display name is limited to a maximum of 21 characters."
        },
        "optional": True,
        "label": {
            "type": "plain_text",
            "text": "Sender Name",
            "emoji": True
        }
    },
    {
        "type": "input",
        "block_id": "icon_url",
        "element": {
            "type": "plain_text_input",
            "action_id": "icon_url-action",
            "placeholder": {
                "type": "plain_text",
                "text": "If left blank, the default icon is used."
            }
        },
        "optional": True,
        "label": {
            "type": "plain_text",
            "text": "Icon URL",
            "emoji": True
        }
    },
    {
        "type": "divider",
        "block_id": "end_sender_identity_fields"
    }
]

call_to_action_dropdown = [
    {
        "type": "divider",
        "block_id": "start_call_to_action_dropdown"
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "How many in-context call action will you need?"
        },
        "block_id": "call_to_action_dropdown",
        "accessory": {
            "type": "static_select",
            "placeholder": {
                "type": "plain_text",
                "text": "Select an item",
                "emoji": True
            },
            "options": [
                {
                    "text": {
                        "type": "plain_text",
                        "text": "1",
                        "emoji": True
                    },
                    "value": "1"
                },
                {
                    "text": {
                        "type": "plain_text",
                        "text": "2",
                        "emoji": True
                    },
                    "value": "2"
                },
                {
                    "text": {
                        "type": "plain_text",
                        "text": "3",
                        "emoji": True
                    },
                    "value": "3"
                }
            ],
            "action_id": "call_to_action_dropdown-action"
        }
    },
    {
        "type": "context",
        "block_id": "cta_buttons_hint",
        "elements": [
            {
                "type": "plain_text",
                "text": "You can add up to three actions.",
                "emoji": True
            }
        ]
    }
]

cta_buttons = [
    {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "CTA Button",
            "emoji": True
        },
        "block_id": "cta_button_header"
    },
    {
        "type": "input",
        "element": {
            "type": "plain_text_input",
            "action_id": "plain_text_input-action"
        },
        "block_id": "cta_button_text",
        "label": {
            "type": "plain_text",
            "text": "Button Text",
            "emoji": True
        },
        "hint": {
            "type": "plain_text",
            "text": "The character limit for button text in a Slack Block Kit button element is 75 characters. The text may appear truncated around 30 characters depending on the display device."
        }
    },
    {
        "type": "input",
        "element": {
            "type": "plain_text_input",
            "action_id": "plain_text_input-action",
            "placeholder": {
                "type": "plain_text",
                "text": "Enter a URL"
            }
        },
        "block_id": "cta_button_link",
        "label": {
            "type": "plain_text",
            "text": "Link",
            "emoji": True
        },
        "hint": {
            "type": "plain_text",
            "text": "Please provide a valid URL (including http:// or https://)."
        }
    }
]

def generate_cta_buttons(num_buttons):
    import copy
    blocks = []
    for i in range(num_buttons):
        cta_buttons_with_unique_block_id = copy.deepcopy(cta_buttons)
        # header
        cta_buttons_with_unique_block_id[0]["block_id"] = f"cta_button_header_{i+1}"
        cta_buttons_with_unique_block_id[0]["text"]["text"] = f"CTA Button {i+1}"
        # button text input
        cta_buttons_with_unique_block_id[1]["block_id"] = f"cta_button_text_{i+1}"
        cta_buttons_with_unique_block_id[1]["label"]["text"] = f"Button Text {i+1}"
        # button link input
        cta_buttons_with_unique_block_id[2]["block_id"] = f"cta_button_link_{i+1}"
        cta_buttons_with_unique_block_id[2]["label"]["text"] = f"Link {i+1}"
        # append to blocks
        blocks += cta_buttons_with_unique_block_id
    return blocks

@app.shortcut("bt_comms_shortcut")
def open_modal(ack, body, client, logger, shortcut):
    # Acknowledge the shortcut request
    ack()
    logger.info(body)
    modal_view = [*initial_view_blocks, *advanced_options_blocks]
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

@app.action("customize_sender_identity-action")
def handle_customize_sender_id_checkbox(ack, body, logger):
    ack()
    logger.info(body)
    modal_view = [*initial_view_blocks, *advanced_options_blocks]
    advanced_options_blocks_with_cta_only = [*initial_view_blocks, *advanced_options_blocks, *call_to_action_dropdown]
    advanced_options_blocks_with_sender_only = [*initial_view_blocks, advanced_options_blocks[0], *sender_identity_fields, advanced_options_blocks[1]]
    advanced_options_blocks_with_sender_and_cta = [*initial_view_blocks, advanced_options_blocks[0], *sender_identity_fields, advanced_options_blocks[1], *call_to_action_dropdown]
    
    customize_sender_identity_selected = body["actions"][0]["selected_options"]
    call_to_action_selected = body["view"]["state"]["values"]["call_to_action"]["call_to_action-action"].get("selected_options", [])
    
    call_to_action_buttons_selected = body["view"]["state"]["values"].get("call_to_action_dropdown", None)

    logger.info("--------------------------------\n")
    if customize_sender_identity_selected:
        logger.info(f"\n customize_sender_identity_selected: {customize_sender_identity_selected}\n")
        logger.info("\nCONDITIONAL CHECKS FOR CUSTOMIZE SENDER ID SELECTED\n")
        logger.info("customize_sender_identity checked.\n")
        if call_to_action_buttons_selected:
            logger.info("CTA BUTTONS TOGGLE DETECTED\n")
            try:
                number_of_cta_buttons = body["view"]["state"]["values"].get("call_to_action_dropdown").get("call_to_action_dropdown-action").get("selected_option").get("value", None)
                logger.info(f"\nNUMBER OF CTA BUTTONS: {number_of_cta_buttons}\n")
                blocks = advanced_options_blocks_with_sender_and_cta + generate_cta_buttons(int(number_of_cta_buttons))
            except:
                blocks = advanced_options_blocks_with_sender_and_cta
        elif call_to_action_selected:
            logger.info("call_to_action checked.\n")
            blocks = advanced_options_blocks_with_sender_and_cta
        else:
            blocks = advanced_options_blocks_with_sender_only
    elif call_to_action_selected:
        logger.info("\nCONDITIONAL CHECKS FOR CALL TO ACTION SELECTED\n")
        logger.info("call_to_action checked.\n")
        if call_to_action_buttons_selected:
            logger.info("CTA BUTTONS TOGGLE DETECTED\n")
            try:
                number_of_cta_buttons = body["view"]["state"]["values"].get("call_to_action_dropdown").get("call_to_action_dropdown-action").get("selected_option").get("value", None)
                logger.info(f"\nNUMBER OF CTA BUTTONS: {number_of_cta_buttons}\n")
                blocks = advanced_options_blocks_with_cta_only + generate_cta_buttons(int(number_of_cta_buttons))
            except:
                blocks = advanced_options_blocks_with_cta_only
        else:
            blocks = advanced_options_blocks_with_cta_only
    else:
        logger.info("\nCONDITIONAL CHECKS FOR BOTH CHECKBOXES UNCHECKED\n")
        logger.info("both checkboxes unchecked. removing all extra fields\n")
        blocks = modal_view
    logger.info("--------------------------------\n")

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
    logger.info(body)

    modal_view = [*initial_view_blocks, *advanced_options_blocks]
    advanced_options_blocks_with_cta_only = [*initial_view_blocks, *advanced_options_blocks, *call_to_action_dropdown]
    advanced_options_blocks_with_sender_only = [*initial_view_blocks, advanced_options_blocks[0], *sender_identity_fields, advanced_options_blocks[1]]
    advanced_options_blocks_with_sender_and_cta = [*initial_view_blocks, advanced_options_blocks[0], *sender_identity_fields, advanced_options_blocks[1], *call_to_action_dropdown]
    
    call_to_action_selected = body["actions"][0]["selected_options"]
    customize_sender_identity_selected = body["view"]["state"]["values"]["customize_sender_identity"]["customize_sender_identity-action"].get("selected_options", [])
    if not call_to_action_selected:
        logger.info("--------------------------------\n")
        logger.info("call_to_action unchecked. removing call_to_action_dropdown\n")
        if not customize_sender_identity_selected:
            logger.info("--------------------------------\n")
            logger.info("also customize_sender_identity is unchecked. removing all extra fields\n")
            blocks = modal_view
        else:
            blocks = advanced_options_blocks_with_sender_only
    elif not customize_sender_identity_selected:
        logger.info("--------------------------------\n")
        logger.info("also customize_sender_identity is unchecked. removing all extra fields\n")
        blocks = advanced_options_blocks_with_cta_only
    else:
        blocks = advanced_options_blocks_with_sender_and_cta
   
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

@app.action("call_to_action_dropdown-action")
def handle_call_to_action_dropdown_action(ack, body, logger):
    ack()
    logger.info(body)

    call_to_action_dropdown_selected = body["actions"][0]["selected_option"]
    call_to_action_requested_buttons = body["actions"][0]["selected_option"]["value"]
    call_to_action_button_blocks = generate_cta_buttons(int(call_to_action_requested_buttons))

    advanced_options_blocks_with_cta_buttons_only = [*initial_view_blocks, *advanced_options_blocks, *call_to_action_dropdown, *call_to_action_button_blocks]
    advanced_options_blocks_with_sender_and_cta_buttons = [*initial_view_blocks, advanced_options_blocks[0], *sender_identity_fields, advanced_options_blocks[1], *call_to_action_dropdown, *call_to_action_button_blocks]

    customize_sender_identity_selected = body["view"]["state"]["values"]["customize_sender_identity"]["customize_sender_identity-action"].get("selected_options", [])

    if call_to_action_dropdown_selected:
        if not customize_sender_identity_selected:
            logger.info("--------------------------------\n")
            logger.info("CUSTOMIZE SENDER ID unchecked.\n")
            logger.info(f"CALL TO ACTION DROPDOWN selected option: {call_to_action_dropdown_selected}\n")
            logger.info(f"REQUESTED NUMBER OF BUTTONS: {call_to_action_requested_buttons}\n")
            logger.info("Generating corresponding number of CTA button input fields...\n")
            blocks = advanced_options_blocks_with_cta_buttons_only
        else:
            logger.info("--------------------------------\n")
            logger.info(f"CALL TO ACTION DROPDOWN selected option: {call_to_action_dropdown_selected}\n")
            logger.info(f"REQUESTED NUMBER OF BUTTONS: {call_to_action_requested_buttons}\n")
            logger.info("Generating corresponding number of CTA button input fields...\n")
            blocks = advanced_options_blocks_with_sender_and_cta_buttons


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

@app.action("plain_text_input-action")
def handle_some_action(ack, body, logger):
    ack()
    logger.info(body)

@app.view("initial_view")
def handle_comms_submission_event(ack, body, client, logger, view):
    #ack()
    logger.info(body)
    rich_text_input_value: str = view["state"]["values"]["rich_text_input"]["rich_text_input-action"]["rich_text_value"]

    def generate_cta_button_elements(view, number_of_buttons):
        try:
            elements = []
            for i in range(number_of_buttons):
                button_text = view["state"]["values"][f"cta_button_text_{i+1}"]["plain_text_input-action"]["value"]
                button_link = view["state"]["values"][f"cta_button_link_{i+1}"]["plain_text_input-action"]["value"].strip()
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
            logger.info(f"\nHere are the generated CTA elements: {elements}\n")
            return elements
        except Exception as e:
            logger.error(f"Error generating CTA button elements: {e}")
            return None

    try:
        # add validation for conversation_select_block
        multi_conversations_selected: list = view["state"]["values"]["conversation_select_block"]["conversation_select_action"]["selected_conversations"]
        if not multi_conversations_selected:
            logging.info("\nNO CONVERSATIONS SELECTED\n")
            ack(response_action="errors", errors={
                "conversation_select_block": "Please select at least one conversation to send the message to."
            })
            return
        
        # add validation for CTA button links
        import validators
        number_of_buttons_selected: int = int(view["state"]["values"]["call_to_action_dropdown"]["call_to_action_dropdown-action"]["selected_option"]["value"])
        logger.info(f"\nNUMBER OF BUTTONS SELECTED: {number_of_buttons_selected}\n")
        for i in range(number_of_buttons_selected):
            button_link_value = view["state"]["values"][f"cta_button_link_{i+1}"]["plain_text_input-action"]["value"].strip()
            logging.info(f"\nVALIDATING BUTTON LINK {i+1}: {button_link_value}\n")
            logging.info(f"\nSTARTS WITH HTTP: {button_link_value.startswith('http://')}\n")
            logging.info(f"\nSTARTS WITH HTTPS: {button_link_value.startswith('https://')}\n")
            #if not (button_link_value.startswith("http://") or button_link_value.startswith("https://")):
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
        buttons = generate_cta_button_elements(view, number_of_buttons_selected)
        """
        note to self: 
        validation successful providing valid urls
        running the code causes an exception when running line 564
        WARNING:root: Exception occured: cannot access local variable 'generate_cta_button_elements' where it is not associated with a value
        FIXED: 
        Moved the generate_cta_button_elements function definition above the try block to ensure it's defined before being called.
        """
    except Exception as e:
        logging.warning(f"\n Exception occured: {e}\n")
        ack()
        buttons = None


    
        
    def customize_sender_identity_state(view)->dict|None:
        customize_sender_identity_selected: list = view["state"]["values"]["customize_sender_identity"]["customize_sender_identity-action"].get("selected_options")
        if customize_sender_identity_selected:
            try:
                sender_name_value: str|None= view["state"]["values"].get("sender_name").get("plain_text_input-action").get("value")
            except:
                sender_name_value = None
            try:
                icon_url_value: str|None = view["state"]["values"].get("icon_url").get("icon_url-action").get("value")
            except:
                icon_url_value = None
            return {"sender_name": sender_name_value, "icon_url": icon_url_value}
        return None
    
    def send_message_to_conversation(conversation_id:str, blocks:list, sender_name:str|None=None, icon_url:str|None=None, cta_elements:list|None=None):
        notification_text = "Message from Slack Communications App"
        message_payload = {
            "channel": conversation_id,
            "text": notification_text,
            "blocks": blocks
        }
        if sender_name:
            # Set your bot's user name.
            message_payload["username"] = sender_name
        if icon_url:
            # URL to an image to use as the icon for this message.
            message_payload["icon_url"] = icon_url
        if cta_elements:
            logger.info(f"\nCTA ELEMENTS TO BE ADDED: {cta_elements}\n")
            message_payload["blocks"] = [*blocks, *cta_elements]

        logger.info(f"\nMESSAGE PAYLOAD TO BE SENT: {message_payload}\n")
        client.chat_postMessage(**message_payload)
    
    # Main Logic
    
    sender_identity = customize_sender_identity_state(view)
    if sender_identity is not None:
        for conversation_id in multi_conversations_selected:
            send_message_to_conversation(
                conversation_id=conversation_id,
                blocks=[rich_text_input_value],
                sender_name=sender_identity["sender_name"],
                icon_url=sender_identity["icon_url"],
                cta_elements = buttons
            )
    else:
        for conversation_id in multi_conversations_selected:
            send_message_to_conversation(
                conversation_id=conversation_id,
                blocks=[rich_text_input_value],
                cta_elements = buttons
            )

@app.action("button_action_1")
@app.action("button_action_2")
@app.action("button_action_3")
def button_was_clicked(ack, body, logger):
    ack()
    logger.info(body)

@app.action("multi_conversations_select-action")
def multi_conversations_select_action(ack, body, logger):
    ack()
    logger.info(body)

# Start Bolt app
if __name__ == "__main__":
    SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()
