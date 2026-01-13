"""
Block Kit templates and composition utilities.
"""
import copy

# Initial view blocks
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

# Advanced options blocks
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

# Sender identity fields
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
            "action_id": "sender_name_input-action",
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

# Call to action dropdown
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

# CTA button template
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
            "action_id": "cta_button_text_input-action"
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
            "action_id": "cta_button_link_input-action",
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
    """
    Generate CTA button input blocks.
    
    Args:
        num_buttons: Number of CTA button groups to generate (1-3)
    
    Returns:
        List of block dictionaries for CTA button inputs
    """
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


def compose_modal_blocks(include_sender_identity=False, include_cta_dropdown=False, num_cta_buttons=0):
    """
    Compose modal blocks based on selected options.
    
    Args:
        include_sender_identity: Whether to include sender identity fields
        include_cta_dropdown: Whether to include call-to-action dropdown
        num_cta_buttons: Number of CTA button input groups to include (0-3)
    
    Returns:
        List of blocks for the modal view
    """
    blocks = [*initial_view_blocks]
    
    if include_sender_identity and include_cta_dropdown:
        # Both options selected
        blocks.extend([advanced_options_blocks[0], *sender_identity_fields, advanced_options_blocks[1], *call_to_action_dropdown])
    elif include_sender_identity:
        # Only sender identity selected
        blocks.extend([advanced_options_blocks[0], *sender_identity_fields, advanced_options_blocks[1]])
    elif include_cta_dropdown:
        # Only CTA dropdown selected
        blocks.extend([*advanced_options_blocks, *call_to_action_dropdown])
    else:
        # Neither selected
        blocks.extend(advanced_options_blocks)
    
    # Add CTA button input fields if specified
    if num_cta_buttons > 0:
        blocks.extend(generate_cta_buttons(num_cta_buttons))
    
    return blocks
