import re
from typing import Dict, Optional

class EmailParser:
    def __init__(self):
        # Email regex pattern
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        # Subject patterns - looking for quoted and unquoted text after "subject"
        self.subject_patterns = [
            # Quoted subjects (higher priority)
            r'subject\s+["\']([^"\']+)["\']',
            r'with\s+the\s+subject\s+["\']([^"\']+)["\']',
            r'subject\s+line\s+["\']([^"\']+)["\']',
            r'title\s+["\']([^"\']+)["\']',
            # Unquoted subjects (capture until comma, "saying", or end)
            r'with\s+the\s+subject\s+([^,]+?)(?:\s*,|\s+saying|\s*$)',
            r'subject\s+([^,]+?)(?:\s*,|\s+saying|\s*$)',
            r'subject\s+line\s+([^,]+?)(?:\s*,|\s+saying|\s*$)'
        ]
        
        # Recipient patterns
        self.recipient_patterns = [
            r'(?:send|email)\s+(?:an?\s+)?email\s+to\s+(\S+@\S+)',
            r'email\s+(\S+@\S+)',
            r'to\s+(\S+@\S+)',
            r'send\s+to\s+(\S+@\S+)'
        ]
        
        # Body extraction patterns - content after "saying" or similar
        self.body_patterns = [
            r'saying\s+["\']([^"\']+)["\']',
            r'saying\s+(.+?)(?:\s+with\s+subject|\s+to\s+\S+@|\s*$)',
            r'message\s+["\']([^"\']+)["\']',
            r'tell\s+them\s+["\']([^"\']+)["\']',
            r'body\s+["\']([^"\']+)["\']'
        ]

    def parse_email_request(self, message: str) -> Dict[str, Optional[str]]:
        """
        Parse a natural language message to extract email components.
        
        Returns:
            Dict with keys: 'recipient', 'subject', 'body', 'error'
        """
        result = {
            'recipient': None,
            'subject': None,
            'body': None,
            'error': None
        }
        
        message_lower = message.lower()
        
        # Extract recipient email
        result['recipient'] = self._extract_recipient(message)
        
        # Extract subject
        result['subject'] = self._extract_subject(message_lower)
        
        # Extract body
        result['body'] = self._extract_body(message, message_lower)
        
        # Validate that we at least have a recipient
        if not result['recipient']:
            result['error'] = "I couldn't find a recipient email address. Please specify who to send the email to (e.g., 'send email to user@example.com')."
        
        return result

    def _extract_recipient(self, message: str) -> Optional[str]:
        """Extract recipient email address from message."""
        # First try recipient-specific patterns
        for pattern in self.recipient_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                email = match.group(1)
                if re.match(self.email_pattern, email):
                    return email
        
        # Fall back to finding any email address
        emails = re.findall(self.email_pattern, message)
        if emails:
            return emails[0]
        
        return None

    def _extract_subject(self, message_lower: str) -> Optional[str]:
        """Extract subject from message."""
        for pattern in self.subject_patterns:
            match = re.search(pattern, message_lower)
            if match:
                return match.group(1).strip()
        
        return None

    def _extract_body(self, message: str, message_lower: str) -> Optional[str]:
        """Extract email body from message."""
        for pattern in self.body_patterns:
            match = re.search(pattern, message_lower)
            if match:
                # Find corresponding position in original message
                original_match = re.search(pattern, message, re.IGNORECASE)
                if original_match:
                    return original_match.group(1).strip()
        
        # If no specific body pattern found, try to extract everything after "saying"
        saying_match = re.search(r'saying\s+(.+?)(?:\s+with\s+subject|\s+to\s+\S+@|\s*$)', message_lower)
        if saying_match:
            # Find original case version
            original_saying = re.search(r'saying\s+(.+?)(?:\s+with\s+subject|\s+to\s+\S+@|\s*$)', message, re.IGNORECASE)
            if original_saying:
                body = original_saying.group(1).strip()
                # Remove quotes if present
                if body.startswith('"') and body.endswith('"'):
                    body = body[1:-1]
                elif body.startswith("'") and body.endswith("'"):
                    body = body[1:-1]
                return body
        
        return None

    def validate_email(self, email: str) -> bool:
        """Validate if a string is a proper email address."""
        return bool(re.match(self.email_pattern, email))