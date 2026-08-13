import json
import re
import os
from datetime import datetime, timedelta

class NLParserService:
    """
    Natural Language Parser service.
    In a real implementation, this would call an LLM (like Groq or NVIDIA NIM) 
    to parse the natural language request into a structured workflow JSON.
    For this implementation, we use rule-based parsing with regex patterns.
    """
    
    def __init__(self):
        # Common trigger words
        self.schedule_triggers = ['every', 'daily', 'weekly', 'monthly', 'each', 'at']
        self.webhook_triggers = ['when', 'if', 'triggered by', 'webhook']
        self.manual_triggers = ['run', 'execute', 'start', 'begin']
        
        # Common sources
        self.sources = {
            'erp': ['college erp', 'school erp', 'university erp', 'erp system', 'sap', 'oracle'],
            'email': ['email', 'gmail', 'outlook', 'mail'],
            'database': ['database', 'db', 'sql', 'mysql', 'postgresql'],
            'file': ['file', 'csv', 'excel', 'spreadsheet'],
            'api': ['api', 'rest', 'webservice', 'endpoint']
        }
        
        # Common actions
        self.actions = {
            'email': ['email', 'send email', 'notify', 'message'],
            'file': ['save file', 'export', 'download', 'write file'],
            'database': ['save to database', 'store in db', 'insert', 'update'],
            'notification': ['notify', 'alert', 'push notification', 'sms'],
            'report': ['generate report', 'create report', 'summarize', 'analytics']
        }
    
    def parse(self, nl_text):
        """
        Parse natural language text into a structured workflow JSON.
        
        Args:
            nl_text (str): The natural language description of the workflow.
            
        Returns:
            dict: A dictionary representing the structured workflow.
        """
        nl_text = nl_text.lower().strip()
        
        # Extract trigger type
        trigger_type = self._extract_trigger_type(nl_text)
        
        # Extract source
        source = self._extract_source(nl_text)
        
        # Extract condition/timing
        condition = self._extract_condition(nl_text, trigger_type)
        
        # Extract action
        action = self._extract_action(nl_text)
        
        # Extract details
        details = self._extract_details(nl_text)
        
        # Build the workflow structure
        workflow_data = {
            "trigger": trigger_type,
            "source": source.title() if source else "Unknown",
            "condition": condition,
            "action": action.title() if action else "Unknown",
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        
        return workflow_data
    
    def _extract_trigger_type(self, text):
        """Extract the trigger type from the text."""
        # Check for schedule triggers
        for trigger in self.schedule_triggers:
            if trigger in text:
                # Look for time patterns
                if re.search(r'\d{1,2}:\d{2}', text) or \
                   re.search(r'(am|pm)', text) or \
                   'morning' in text or 'afternoon' in text or 'evening' in text:
                    return "schedule"
                # Look for frequency patterns
                if re.search(r'every \d+', text) or \
                   'daily' in text or 'weekly' in text or 'monthly' in text or \
                   'hourly' in text:
                    return "schedule"
                    
        # Check for webhook triggers
        for trigger in self.webhook_triggers:
            if trigger in text:
                return "webhook"
                
        # Default to manual
        return "manual"
    
    def _extract_source(self, text):
        """Extract the source from the text."""
        for source, keywords in self.sources.items():
            for keyword in keywords:
                if keyword in text:
                    return source
        # If no specific source found, try to extract a noun phrase
        words = text.split()
        for i, word in enumerate(words):
            if word in ['from', 'of', 'in', 'at'] and i+1 < len(words):
                return words[i+1]
        return "external system"
    
    def _extract_condition(self, text, trigger_type):
        """Extract the condition or timing from the text."""
        if trigger_type == "schedule":
            # Look for time patterns
            time_match = re.search(r'(\d{1,2}:\d{2}\s*(am|pm)?)', text)
            if time_match:
                return f"At {time_match.group(1)}"
            
            # Look for frequency patterns
            if 'daily' in text:
                return "Daily"
            elif 'weekly' in text:
                return "Weekly"
            elif 'monthly' in text:
                return "Monthly"
            elif 'hourly' in text:
                return "Hourly"
            elif re.search(r'every \d+ (minutes?|hours?|days?)', text):
                match = re.search(r'every (\d+ (minutes?|hours?|days?))', text)
                return f"Every {match.group(1)}"
                
            return "On schedule"
        elif trigger_type == "webhook":
            return "When webhook is received"
        else:
            return "Manual trigger"
    
    def _extract_action(self, text):
        """Extract the action from the text."""
        for action, keywords in self.actions.items():
            for keyword in keywords:
                if keyword in text:
                    return action
        # If no specific action found, look for verb phrases
        action_verbs = ['send', 'save', 'create', 'generate', 'update', 'delete', 'fetch', 'get']
        for verb in action_verbs:
            if verb in text:
                # Find the object of the verb
                words = text.split()
                try:
                    idx = words.index(verb)
                    if idx + 1 < len(words):
                        return f"{verb} {words[idx+1]}"
                except ValueError:
                    pass
                return verb
        return "process data"
    
    def _extract_details(self, text):
        """Extract additional details from the text."""
        details = []
        
        # Extract any quoted text or specific parameters
        quoted = re.findall(r'"([^"]*)"', text)
        if quoted:
            details.extend(quoted)
            
        # Extract numbers with units
        numbers_with_units = re.findall(r'\d+\s*(minutes?|hours?|days?|weeks?|months?)', text)
        if numbers_with_units:
            details.extend(numbers_with_units)
            
        # Extract email addresses
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        if emails:
            details.extend(emails)
            
        # If we have details, join them; otherwise return a generic message
        if details:
            return "; ".join(details)
        else:
            return f"Process extracted from: '{text[:50]}{'...' if len(text) > 50 else ''}'"

# Create a singleton instance for easy access
nl_parser_service = NLParserService()
