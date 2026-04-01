from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from config import Config

def test_slack_auth():
    """Test Slack bot authentication."""
    try:
        client = WebClient(token=Config.get_bot_token())
        response = client.auth_test()

        print("✓ Auth test passed!")
        print(f"  Bot ID: {response['user_id']}")
        print(f"  Bot Name: {response['user']}")
        print(f"  Team: {response['team']}")
        print(f"  Team ID: {response['team_id']}")

    except SlackApiError as e:
        print(f"✗ Auth test failed: {e.response['error']}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")

if __name__ == "__main__":
    test_slack_auth()