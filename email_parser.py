import re
from typing import Dict, Optional, List

class EmailParser:
    def __init__(self):
        # Email regex pattern
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        # Subject keywords to identify where subject starts
        self.subject_keywords = [
            'with subject', 'with a subject', 'with the subject',
            'subject', 'subject line', 'titled', 'title', 'called',
            'with title', 'with the title', 'labeled', 'label'
        ]
        
        # Body keywords that indicate message content
        self.body_keywords = [
            'saying', 'message', 'tell them', 'body', 'content',
            'text', 'write', 'send them', 'let them know'
        ]
        
        # Command keywords that start email requests
        self.command_keywords = [
            'email', 'send email', 'send an email', 'send',
            'compose', 'write email', 'mail'
        ]

    def parse_email_request(self, message: str) -> Dict[str, Optional[str]]:
        """
        Parse a natural language message to extract email components using contextual analysis.
        
        Returns:
            Dict with keys: 'recipient', 'subject', 'body', 'error'
        """
        result = {
            'recipient': None,
            'subject': None,
            'body': None,
            'error': None
        }
        
        # Use new natural language processing approach
        parsed_components = self._parse_natural_language(message)
        
        result['recipient'] = parsed_components.get('recipient')
        result['subject'] = parsed_components.get('subject')
        result['body'] = parsed_components.get('body')
        
        # Validate that we at least have a recipient
        if not result['recipient']:
            result['error'] = "I couldn't find a recipient email address. Please specify who to send the email to (e.g., 'send email to user@example.com')."
        
        return result

    def _parse_natural_language(self, message: str) -> Dict[str, Optional[str]]:
        """
        Parse message using contextual natural language processing.
        
        Args:
            message: The input message to parse
            
        Returns:
            Dict with extracted components: recipient, subject, body
        """
        result = {'recipient': None, 'subject': None, 'body': None}
        
        # Find email address first as it's our anchor point
        emails = re.findall(self.email_pattern, message)
        if emails:
            result['recipient'] = emails[0]
        else:
            return result
        
        # Split message into tokens for analysis
        message_lower = message.lower()
        
        # Find subject using expanded keyword matching
        result['subject'] = self._extract_subject_contextual(message, message_lower)
        
        # Extract body content using positional and contextual analysis
        result['body'] = self._extract_body_contextual(message, message_lower, result['recipient'], result['subject'])
        
        return result
    
    def _extract_subject_contextual(self, message: str, message_lower: str) -> Optional[str]:
        """Extract subject using contextual keyword matching."""
        # Sort subject keywords by length (longer phrases first for better matching)
        sorted_keywords = sorted(self.subject_keywords, key=len, reverse=True)
        
        for keyword in sorted_keywords:
            # Find the keyword in the message
            keyword_pos = message_lower.find(keyword)
            if keyword_pos != -1:
                # Start extracting after the keyword
                start_pos = keyword_pos + len(keyword)
                
                # Find where to stop - look for body separator keywords
                end_pos = len(message)  # Default to end of message
                
                # Check for body keywords that should terminate subject extraction
                for body_keyword in self.body_keywords:
                    body_pos = message_lower.find(body_keyword, start_pos)
                    if body_pos != -1 and body_pos < end_pos:
                        end_pos = body_pos
                
                # Also stop at comma followed by body keywords (common pattern)
                comma_saying_match = re.search(r',\s*saying', message_lower[start_pos:])
                if comma_saying_match:
                    comma_pos = start_pos + comma_saying_match.start()
                    if comma_pos < end_pos:
                        end_pos = comma_pos
                
                subject_text = message[start_pos:end_pos].strip()
                
                # Remove leading non-alphanumeric characters
                subject_text = re.sub(r'^[^\w"\']+', '', subject_text)
                
                # Remove trailing punctuation (especially commas)
                subject_text = re.sub(r'[,\s]+$', '', subject_text)
                
                # Remove quotes if present
                if subject_text.startswith('"') and subject_text.endswith('"'):
                    subject_text = subject_text[1:-1]
                elif subject_text.startswith("'") and subject_text.endswith("'"):
                    subject_text = subject_text[1:-1]
                
                if subject_text:
                    return subject_text.strip()
        
        return None
    
    def _extract_body_contextual(self, message: str, message_lower: str, recipient: str, subject: Optional[str]) -> Optional[str]:
        """Extract body using contextual analysis and positioning."""
        if not recipient:
            return None
        
        # Method 1: Look for explicit body keywords
        for keyword in self.body_keywords:
            keyword_pos = message_lower.find(keyword)
            if keyword_pos != -1:
                # Extract content after the keyword
                start_pos = keyword_pos + len(keyword)
                
                # Find where to stop (before subject keywords or end)
                end_pos = len(message)
                for subj_keyword in self.subject_keywords:
                    subj_pos = message_lower.find(subj_keyword, start_pos)
                    if subj_pos != -1 and subj_pos < end_pos:
                        end_pos = subj_pos
                
                body_text = message[start_pos:end_pos].strip()
                body_text = re.sub(r'^[^\w"\']+', '', body_text)  # Remove leading punctuation
                
                # Remove quotes
                if body_text.startswith('"') and body_text.endswith('"'):
                    body_text = body_text[1:-1]
                elif body_text.startswith("'") and body_text.endswith("'"):
                    body_text = body_text[1:-1]
                
                if body_text:
                    return body_text.strip()
        
        # Method 2: Extract content between email and subject keywords (positional analysis)
        email_pos = message_lower.find(recipient.lower())
        if email_pos != -1:
            # Start looking after the email address
            search_start = email_pos + len(recipient)
            
            # Find the earliest subject keyword position
            subject_start = len(message)  # Default to end of message
            for subj_keyword in self.subject_keywords:
                subj_pos = message_lower.find(subj_keyword, search_start)
                if subj_pos != -1 and subj_pos < subject_start:
                    subject_start = subj_pos
            
            # Extract content between email and subject
            if subject_start > search_start:
                body_text = message[search_start:subject_start].strip()
                
                # Clean up the extracted text
                body_text = re.sub(r'^[^\w"\']+', '', body_text)  # Remove leading punctuation
                body_text = re.sub(r'[^\w"\']+$', '', body_text)  # Remove trailing punctuation
                
                # Remove quotes
                if body_text.startswith('"') and body_text.endswith('"'):
                    body_text = body_text[1:-1]
                elif body_text.startswith("'") and body_text.endswith("'"):
                    body_text = body_text[1:-1]
                
                if body_text and len(body_text) > 0:
                    return body_text.strip()
        
        return None

    def validate_email(self, email: str) -> bool:
        """Validate if a string is a proper email address."""
        return bool(re.match(self.email_pattern, email))