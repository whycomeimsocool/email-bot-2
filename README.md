# Discord Email Bot

A Discord bot that prepares emails on your behalf using natural language processing. Simply tell the bot what email you want to send, and it will parse your message and open your default email client with all the fields pre-filled.

## Features

- 🤖 Natural language processing to extract email components
- 📧 Automatic email client integration using mailto: URLs
- 🎯 Smart parsing of recipient, subject, and body from conversational text
- ✅ Error handling and clarification requests
- 🔄 Support for message edits

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Discord Bot

1. Go to https://discord.com/developers/applications
2. Click "New Application" and give it a name
3. Go to the "Bot" section in the left sidebar
4. Click "Add Bot"
5. Under "Token", click "Copy" to copy your bot token
6. Under "Privileged Gateway Intents", enable "Message Content Intent"

### 3. Configure Environment

1. Open the `.env` file
2. Replace `YOUR_BOT_TOKEN_HERE` with your actual Discord bot token:
   ```
   DISCORD_TOKEN=your_actual_bot_token_here
   ```

### 4. Invite Bot to Server

1. In Discord Developer Portal, go to "OAuth2" → "URL Generator"
2. Select "bot" scope
3. Select these bot permissions:
   - Send Messages
   - Read Message History
   - Use Slash Commands (optional)
4. Copy the generated URL and visit it to invite the bot to your server

### 5. Run the Bot

```bash
python bot.py
```

## Usage Examples

The bot responds to messages that either mention the bot directly or contain the word "email". Here are some example commands:

### Basic Email
```
@EmailBot send an email to john@example.com saying see you tomorrow!
```

### Email with Subject
```
@EmailBot send an email with the subject "Meeting Tomorrow" to sarah@company.com saying "Don't forget about our 2pm meeting"
```

### Various Phrasings
```
hey bot, email user@domain.com saying hello there!

bot please send an email to contact@business.org with the subject "Question" saying "I have a quick question about your services"

email admin@site.com saying "Thanks for your help!"
```

## How It Works

1. **Message Detection**: Bot listens for messages mentioning it or containing "email"
2. **Natural Language Processing**: Uses regex patterns to extract:
   - Recipient email address
   - Subject line (from quoted text after "subject")
   - Email body (from text after "saying" or similar phrases)
3. **Email Preview**: Shows a formatted preview of the parsed email
4. **Email Client Integration**: Opens your default email client with pre-filled fields using mailto: URLs

## File Structure

- `bot.py` - Main Discord bot logic and event handlers
- `email_parser.py` - Natural language processing for email parsing
- `email_handler.py` - Email client integration and mailto URL generation
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (bot token)

## Troubleshooting

### Bot doesn't respond
- Make sure "Message Content Intent" is enabled in Discord Developer Portal
- Check that the bot has permission to read and send messages in the channel
- Verify your bot token is correct in the `.env` file

### Email client doesn't open
- The bot will provide a clickable mailto: link as a fallback
- Some systems may require additional configuration for default email client

### Parsing issues
- The bot will ask for clarification if it can't parse your message
- Try using clearer phrasing like "send email to [address] saying [message]"
- Include quotes around subjects: 'with the subject "Your Subject Here"'

## Contributing

This bot uses regex-based natural language processing. To improve parsing accuracy, you can modify the patterns in `email_parser.py`:

- `recipient_patterns` - For finding email addresses
- `subject_patterns` - For extracting quoted subject lines  
- `body_patterns` - For extracting message content

## License

This project is open source and available under the MIT License.