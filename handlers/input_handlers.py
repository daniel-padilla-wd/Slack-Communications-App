"""
Input action handlers for text inputs and other interactive elements.
"""


def register_input_handlers(app):
    """Register all input-related handlers."""
    
    @app.action("sender_name_input-action")
    @app.action("icon_url_input-action")
    @app.action("cta_button_text_input-action")
    @app.action("cta_button_link_input-action")
    def handle_input_actions(ack, body, logger):
        """Acknowledge modal input interactions to satisfy Slack action flow."""
        ack()
    
    @app.action("button_action_1")
    @app.action("button_action_2")
    @app.action("button_action_3")
    def button_was_clicked(ack, body, logger):
        """Acknowledge CTA button clicks from posted messages."""
        ack()

    @app.action("multi_conversations_select-action")
    def multi_conversations_select_action(ack, body, logger):
        """Acknowledge multi-conversation selection changes in the modal."""
        ack()
