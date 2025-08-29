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
    try:
        print(f"Received message: {message.content[:50]}...")  # Debug log
        
        # Don't respond to the bot's own messages
        if message.author == client.user:
            return
        
        # Check if the message mentions the bot or contains "email"
        bot_mentioned = client.user in message.mentions
        contains_email_keyword = 'email' in message.content.lower()
        
        print(f"Bot mentioned: {bot_mentioned}, Contains email: {contains_email_keyword}")  # Debug log
        
        if not (bot_mentioned or contains_email_keyword):
            return
        
        print("Processing email request...")  # Debug log
        
        # Parse the message for email components
        result = email_parser.parse_email_request(message.content)
        print(f"Parse result: {result}")  # Debug log
        
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
        
        # Create mailto link
        mailto_url = email_handler.create_mailto_url(
            result['recipient'], 
            result['subject'], 
            result['body']
        )
        print(f"Created mailto URL: {mailto_url[:100]}...")  # Debug log
        
        try:
            # Create Discord embed with email preview
            embed = discord.Embed(
                title="📧 Email Preview",
                color=0x00ff00,  # Green color
                url=mailto_url   # Makes the title clickable!
            )
            
            embed.add_field(name="To:", value=result['recipient'], inline=False)
            
            if result['subject']:
                embed.add_field(name="Subject:", value=result['subject'], inline=False)
            else:
                embed.add_field(name="Subject:", value="(blank)", inline=False)
            
            if result['body']:
                # Truncate body if too long for embed
                display_body = result['body'] if len(result['body']) <= 1000 else result['body'][:1000] + "..."
                embed.add_field(name="Body:", value=f"```\n{display_body}\n```", inline=False)
            else:
                embed.add_field(name="Body:", value="(blank)", inline=False)
            
            embed.add_field(
                name="🔗 Open Email Client", 
                value=f"[Click here to open your email client]({mailto_url})", 
                inline=False
            )
            
            embed.set_footer(text="Click the title or the link above to open your email client!")
            
            await message.channel.send(embed=embed)
            print("Sent embed successfully!")  # Debug log
            
        except Exception as embed_error:
            print(f"Embed error: {embed_error}")  # Debug log
            # Fallback to simple text response
            preview = email_handler.format_email_preview(
                result['recipient'], 
                result['subject'], 
                result['body']
            )
            await message.channel.send(f"{preview}\n\n📬 Click this link to open your email client:\n{mailto_url}")
            print("Sent fallback text response")  # Debug log
        
        # Also try to open automatically (but don't rely on it)
        email_handler.open_email_client(
            result['recipient'], 
            result['subject'], 
            result['body']
        )
        
    except Exception as e:
        print(f"Major error in on_message: {e}")  # Debug log
        try:
            await message.channel.send("❌ I encountered an error processing your request. Please try again.")
        except:
            print("Failed to send error message to Discord")  # Debug log

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