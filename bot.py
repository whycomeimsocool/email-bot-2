import discord
import os
from dotenv import load_dotenv
from email_parser import EmailParser
from email_handler import EmailHandler

# Load environment variables
load_dotenv()

# Initialize components
email_parser = EmailParser()
email_handler = EmailHandler()

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    print('Email bot is ready to help with email preparation!')

@client.event
async def on_message(message):
    # Don't respond to the bot's own messages
    if message.author == client.user:
        return
    
    # Check if the message mentions the bot or contains "email"
    bot_mentioned = client.user in message.mentions
    contains_email_keyword = 'email' in message.content.lower()
    
    if not (bot_mentioned or contains_email_keyword):
        return
    
    # Parse the message for email components
    result = email_parser.parse_email_request(message.content)
    
    # If there's an error, ask for clarification
    if result['error']:
        await message.channel.send(f"❌ {result['error']}")
        return
    
    # If no recipient found, ask for clarification
    if not result['recipient']:
        await message.channel.send(
            "❌ I couldn't find a recipient email address. Please specify who to send the email to.\n"
            "Example: 'send an email to user@example.com saying hello!'"
        )
        return
    
    # Show email preview
    preview = email_handler.format_email_preview(
        result['recipient'], 
        result['subject'], 
        result['body']
    )
    
    await message.channel.send(preview)
    
    # Create and provide mailto link
    mailto_url = email_handler.create_mailto_url(
        result['recipient'], 
        result['subject'], 
        result['body']
    )
    
    await message.channel.send(
        f"📬 Click this link to open your email client:\n{mailto_url}\n\n"
        f"*If the link doesn't work, copy and paste it into your browser's address bar.*"
    )
    
    # Also try to open automatically (but don't rely on it)
    email_handler.open_email_client(
        result['recipient'], 
        result['subject'], 
        result['body']
    )

@client.event
async def on_message_edit(before, after):
    # Treat edited messages as new messages
    await on_message(after)

def main():
    # Get the Discord token from environment variables
    token = os.getenv('DISCORD_TOKEN')
    
    if not token:
        print("Error: DISCORD_TOKEN not found in environment variables.")
        print("Please make sure you have a .env file with your Discord bot token.")
        print("Example: DISCORD_TOKEN=your_bot_token_here")
        return
    
    if token == "YOUR_BOT_TOKEN_HERE":
        print("Error: Please replace YOUR_BOT_TOKEN_HERE with your actual Discord bot token in the .env file.")
        return
    
    try:
        client.run(token)
    except discord.LoginFailure:
        print("Error: Invalid Discord token. Please check your .env file.")
    except Exception as e:
        print(f"Error starting bot: {e}")

if __name__ == "__main__":
    main()