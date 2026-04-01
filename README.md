# BT Comms App

## Overview

BT Comms App is a Slack Bolt (Python) app that lets a user compose a rich-text message in a modal and send it to multiple Slack conversations.

Implemented capabilities:
- Global shortcut: `bt_comms_shortcut`
- Rich text input for message body
- Multi-conversation target selection
- Optional sender customization (`username`, `icon_url`)
- Optional CTA buttons (1 to 3 buttons with URLs)
- URL validation for icon URL and CTA links
- Optional shortcut access gating in production mode

Runtime entry points:
- Local: Socket Mode via `python3 app.py`
- Production (EC2): run `app.py` as a long-lived process

## Runtime Behavior

### Current behavior in code

- App runs in Socket Mode when started with `python3 app.py`.
- Configuration currently uses local environment values for `S_BOT_TOKEN`, `S_APP_TOKEN`, and `S_SIGNING_SECRET`.
- `Config.PRODUCTION` is hardcoded to `False`, so AWS secret retrieval is not active in current runtime behavior.
- `aws_secrets.py` exists, but this path is inactive unless production behavior is enabled in code.

### Target behavior for EC2 production

- App runs as a long-lived Socket Mode process on EC2.
- AWS Secrets Manager is the primary source for bot token and signing secret.
- Local environment variables remain available as fallback values.
- App runs under a process manager (for example, `systemd` or `supervisor`) with centralized logs.

### Gap between current and target

- Production mode toggle is not currently externalized.
- AWS secret retrieval path is present but not active by default.
- Secret parsing and region handling should be hardened before full production rollout.

### Suggested EC2 rollout checklist

1. Confirm secret names and region in AWS Secrets Manager.
2. Keep fallback env vars available on the EC2 instance.
3. Configure process supervision and restart policy.
4. Validate startup, shortcut open, submission, and message delivery in a test workspace.

## Architecture

### Core Modules

- `app.py`
    - Initializes Slack Bolt app with `process_before_response=True`
    - Registers handler groups from `handlers/`
    - Starts `SocketModeHandler(app, APP_TOKEN).start()` when run as script
- `config.py`
    - Loads `.env`
    - Resolves `BOT_TOKEN`, `SIGNING_SECRET`, `APP_TOKEN`, `SSL_CONTEXT`
    - Defines optional user allowlist from `ALLOWED_SHORTCUT_USER_IDS`
- `aws_secrets.py`
    - Retrieves secret values from AWS Secrets Manager
- `blocks/__init__.py`
    - Defines modal block templates
    - Builds dynamic modal content via `compose_modal_blocks(...)`
    - Builds CTA input sections via `generate_cta_buttons(...)`
- `services/__init__.py`
    - Builds CTA message blocks via `generate_cta_button_elements(...)`
    - Extracts sender customization state via `customize_sender_identity_state(...)`
    - Sends messages via `send_message_to_conversation(...)`
- `handlers/`
    - `modal_handlers.py`: shortcut listener and authorization middleware
    - `checkbox_handlers.py`: dynamic modal rebuild on checkbox state
    - `dropdown_handlers.py`: dynamic CTA button count updates
    - `input_handlers.py`: acknowledgement handlers for interactive inputs/buttons
    - `submission_handlers.py`: submit-time validation and dispatch loop

## Request Flow

1. User triggers global shortcut `bt_comms_shortcut`.
2. If production mode is enabled, middleware validates user ID against `ALLOWED_SHORTCUT_USER_IDS`.
3. App opens modal with callback ID `initial_view`.
4. Checkbox and dropdown actions update modal blocks dynamically.
5. On submit:
     - Validates at least one selected conversation.
     - Validates icon URL (if provided).
     - Validates CTA links (if CTA is enabled).
6. App posts message to each selected conversation.
7. On post failure, app sends a warning DM to the caller.

## Slack Manifest Expectations

From `manifest.json`:
- Global shortcut callback ID: `bt_comms_shortcut`
- Interactivity enabled
- Socket Mode enabled
- Bot scopes:
    - `chat:write`
    - `commands`
    - `users:read.email`
    - `users:read`
    - `chat:write.customize`
    - `chat:write.public`

Operational note:
- For private channels, add the app to the channel before posting.

## Dependencies

From `requirements.txt`:
- `slack_bolt`
- `slack_sdk`
- `python-dotenv`
- `certifi`
- `validators`
- `boto3`
- `flask`

## Local Setup

### 1) Create and install the Slack app

1. Open https://api.slack.com/apps/new and choose "From an app manifest".
2. Select your workspace.
3. Paste `manifest.json` content.
4. Create and install the app.

### 2) Create `.env`

The current code reads these variables:

```bash
# Primary values for local development
S_BOT_TOKEN=xoxb-...
S_APP_TOKEN=xapp-...
S_SIGNING_SECRET=...
ALLOWED_SHORTCUT_USER_IDS=U12345,U67890
```

Notes:
- `ALLOWED_SHORTCUT_USER_IDS` is optional and used only when production mode is enabled.
- For EC2 production, use AWS Secrets Manager as the primary credential source.
- Keep `S_BOT_TOKEN`, `S_APP_TOKEN`, and `S_SIGNING_SECRET` as environment fallback values.

### 3) Install and run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

## Production Deployment (EC2)

Production is intended to run on an EC2 instance as a long-running process.

Recommended approach:
- Use Socket Mode and start the app with `python3 app.py`.
- Store bot token and signing secret in AWS Secrets Manager.
- Keep `S_BOT_TOKEN`, `S_APP_TOKEN`, and `S_SIGNING_SECRET` available on the instance as fallback values.
- If using non-default region, ensure secrets are in the region expected by code (`us-west-2`).
- Run the app under a process manager (for example, `systemd` or `supervisor`) so it restarts automatically.
- Centralize logs for operational monitoring.

## Known Caveats (Current Implementation)

These are based on current source behavior:

1. `Config.PRODUCTION` is hardcoded to `False` in `config.py`.
    - This means the AWS Secrets production path is not active unless the code is changed.

2. CTA URL validation in `submission_handlers.py` derives selected CTA button count from string length of selected value.
     - This can under-validate links for selections above one button.

3. `aws_secrets.get_secret_string` uses `eval(...)` and returns the first key value from `SecretString`.

4. AWS Secrets Manager region is currently hardcoded to `us-west-2`.

## Troubleshooting

- "Access denied" modal appears:
    - Verify caller user ID and `ALLOWED_SHORTCUT_USER_IDS`.

- Messages fail to post to a conversation:
    - Ensure the app is installed in the workspace and added to private channels.
    - Check app scopes from `manifest.json`.

- URL validation errors on submit:
    - Ensure links include `http://` or `https://`.
