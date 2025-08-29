import webbrowser
import urllib.parse
from typing import Optional

class EmailHandler:
    def __init__(self):
        pass

    def create_mailto_url(self, recipient: str, subject: Optional[str] = None, body: Optional[str] = None) -> str:
        """
        Create a mailto URL with the given parameters.
        
        Args:
            recipient: Email address of the recipient
            subject: Optional subject line
            body: Optional email body
            
        Returns:
            Properly formatted mailto URL
        """
        # Start with basic mailto
        mailto_url = f"mailto:{recipient}"
        
        # Collect parameters
        params = {}
        
        if subject:
            params['subject'] = subject
        
        if body:
            params['body'] = body
        
        # If we have parameters, add them to the URL
        if params:
            query_string = urllib.parse.urlencode(params)
            mailto_url += f"?{query_string}"
        
        return mailto_url

    def open_email_client(self, recipient: str, subject: Optional[str] = None, body: Optional[str] = None) -> bool:
        """
        Open the default email client with pre-filled email data.
        
        Args:
            recipient: Email address of the recipient
            subject: Optional subject line
            body: Optional email body
            
        Returns:
            True if successful, False otherwise
        """
        try:
            mailto_url = self.create_mailto_url(recipient, subject, body)
            webbrowser.open(mailto_url)
            return True
        except Exception as e:
            print(f"Error opening email client: {e}")
            return False

    def format_email_preview(self, recipient: str, subject: Optional[str] = None, body: Optional[str] = None) -> str:
        """
        Create a formatted preview of the email for Discord display.
        
        Args:
            recipient: Email address of the recipient
            subject: Optional subject line
            body: Optional email body
            
        Returns:
            Formatted string showing email details
        """
        preview = "📧 **Email Preview:**\n"
        preview += f"**To:** {recipient}\n"
        
        if subject:
            preview += f"**Subject:** {subject}\n"
        else:
            preview += "**Subject:** (blank)\n"
        
        if body:
            # Truncate body if too long for Discord
            display_body = body if len(body) <= 200 else body[:200] + "..."
            preview += f"**Body:**\n```\n{display_body}\n```"
        else:
            preview += "**Body:** (blank)\n"
        
        return preview