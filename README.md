# BT Comms App - Slack Bolt Application

A modular Slack bot application built with Bolt for Python that enables customized message distribution with sender identity customization and call-to-action buttons.

## Project Structure

### Github

```
Slack-Comms-App/
├── app.py                     # Main application entry point
├── backup_app.py              # Backup of original monolithic implementation
├── config.py                  # Configuration management and environment detection
├── aws_secrets.py             # AWS Secrets Manager integration
├── requirements.txt           # Python dependencies
├── manifest.json              # Slack app manifest
├── .env                       # Environment variables (not in git)
├── README.md                  # This file
│
├── handlers/                  # Event handlers (modular)
│   ├── __init__.py
│   ├── modal_handlers.py      # Modal opening and initialization
│   ├── checkbox_handlers.py   # Sender identity & CTA checkbox interactions
│   ├── dropdown_handlers.py   # CTA button count selection
│   ├── input_handlers.py      # Input field acknowledgments
│   └── submission_handlers.py # View submission & message sending
│
├── blocks/                    # Block Kit templates
│   └── __init__.py            # All block definitions and composition logic
│
├── services/                  # Business logic
│   └── __init__.py            # Message handling and state management
│
├── .slack/                    # Folder comes from Slack CLI template app
```

## AWS Lambda
```
├── app.py
├── config.py
├── aws_secrets.py
├── handlers/
│   ├── modal_handlers.py
│   ├── checkbox_handlers.py
│   ├── dropdown_handlers.py
│   ├── input_handlers.py
│   └── submission_handlers.py
├── blocks/
│   └── __init__.py
└── services/
    └── __init__.py
```

## Architecture

### Main Components

- **app.py**: Entry point that initializes the Slack app, registers handlers, and starts Socket Mode (local) or Lambda handler (production)
- **config.py**: Centralized configuration with environment detection (sandbox vs production/Lambda)
- **aws_secrets.py**: Retrieves credentials from AWS Secrets Manager in production
- **handlers/**: Modular event handlers registered via registration pattern
- **blocks/**: Block Kit UI templates and composition functions
- **services/**: Business logic separated from presentation layer

### Deployment Modes

**Local Development (Socket Mode)**:
- Uses environment variables from `.env` file
- Custom SSL context for development
- Real-time connection via Socket Mode
- Run with: `python3 app.py`

**Production (AWS Lambda)**:
- Retrieves secrets from AWS Secrets Manager
- Uses default SSL context
- HTTP-based via API Gateway + Lambda
- Requires signing secret for request verification
- Handler function: `lambda_handler`

Before getting started, make sure you have a development workspace where you have permissions to install apps. If you don’t have one setup, go ahead and [create one](https://slack.com/create).
## Installation

#### Create a Slack App
1. Open [https://api.slack.com/apps/new](https://api.slack.com/apps/new) and choose "From an app manifest"
2. Choose the workspace you want to install the application to
3. Copy the contents of [manifest.json](./manifest.json) into the text box that says `*Paste your manifest code here*` (within the JSON tab) and click *Next*
4. Review the configuration and click *Create*
5. Click *Install to Workspace* and *Allow* on the screen that follows. You'll then be redirected to the App Configuration dashboard.

#### Environment Variables
Create a `.env` file in the project root with the following variables:

```bash
# Sandbox/Local Development (Socket Mode)
S_BOT_TOKEN=xoxb-your-bot-token
S_APP_TOKEN=xapp-your-app-token
SLACK_SIGNING_SECRET=your-signing-secret

# Production/Lambda Configuration
SANDBOX_MODE=true  # Set to false for production
LOG_LEVEL=INFO     # DEBUG, INFO, WARNING, ERROR

# AWS Secrets Manager (Production Only)
AWS_BOT_TOKEN_SECRET=aws-secret-name
AWS_SIGNING_SECRET_SECRET=aws-secret-name
```

**Getting Slack Tokens:**
1. Open your apps configuration page, click **OAuth & Permissions**, copy the Bot User OAuth Token as `S_BOT_TOKEN`
2. Click **Basic Information**, create an app-level token with `connections:write` scope, copy as `S_APP_TOKEN`
3. Get the Signing Secret from **Basic Information** as `SLACK_SIGNING_SECRET`

### Setup Your Local Project
```zsh
# Clone this project
git clone <your-repo-url>

# Change into project directory
cd busy-lion-512

# Setup python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your tokens (see Environment Variables above)

# Start local server
python3 app.py
```

## Features

- **Customizable Sender Identity**: Override bot name and icon per message
- **Call-to-Action Buttons**: Add up to 3 clickable buttons with external links
- **Multi-Channel Distribution**: Send to multiple channels/DMs simultaneously
- **Rich Text Support**: Full Slack rich text formatting
- **URL Validation**: Automatic validation of CTA button links
- **Environment Flexibility**: Toggle between local dev and production with one variable

## Configuration

The app automatically detects its environment:
- **Sandbox Mode** (`SANDBOX_MODE=true`): Uses Socket Mode with local env vars
- **Production Mode** (`SANDBOX_MODE=false` + AWS Lambda): Fetches secrets from AWS Secrets Manager

## AWS Lambda Deployment

1. Set `SANDBOX_MODE=false` in Lambda environment variables
2. Store credentials in AWS Secrets Manager
3. Configure API Gateway endpoint
4. Update Slack app Request URLs to API Gateway endpoint
5. Ensure Lambda has `secretsmanager:GetSecretValue` IAM permissions

## Development

```zsh
# Run linting
flake8 *.py handlers/ blocks/ services/

# Run the app locally
python3 app.py
```
