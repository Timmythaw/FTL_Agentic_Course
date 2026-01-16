"""
Execution Logic for all tools.
Each function handles the actual business logic, error handling and returns clean messages.
"""

from datetime import datetime
from zoneinfo import ZoneInfo
import json
import re
from typing import Dict, Any

# Hardcoded mapping of city names to timezone identifiers
LOCATION_TIMEZONES = {
    "cape town": "Africa/Johannesburg",
    "capetown": "Africa/Johannesburg",
    "new york": "America/New_York",
    "newyork": "America/New_York",
    "bangkok": "Asia/Bangkok",
    "london": "Europe/London",
    "tokyo": "Asia/Tokyo",
    "utc": "UTC",
}

def execute_get_time(location: str) -> str:
    """
    Get the current time for a specific location.
    Supports at least 3 locations with hardcoded timezone mappings.
    """
    try:
        " Normalize location input"
        location_key = location.lower().strip()

        if location_key not in LOCATION_TIMEZONES:
            available = ", ".join(sorted(set(LOCATION_TIMEZONES.keys())))
            return f"Error: Location '{location}' not supported. Available locations: {available}."
        
        # Get timezone and current time
        tz = ZoneInfo(LOCATION_TIMEZONES[location_key])
        current_time = datetime.now(tz)
        return f"The current time in {location.title()} is {current_time.strftime('%I:%M %p %Z')} on {current_time.strftime('%A, %B %d, %Y')}"
    
    except Exception as e:
        return f"Error retrieving time for {location}: {str(e)}"
    
def execute_calc(expression: str) -> str:
    """
    Calculate mathematical expressions.
    Handles invalid expressions with clean error messages.
    Enhanced error handling.
    """
    try:
        # Handle empty or whitespace-only input
        if not expression or expression.strip() == "":
            return "Error: Empty expression provided. Please provide a mathematical expression to calculate."
        
        # Handle percentage expressions like "18% of 24500"
        percentage_pattern = r'(\d+(?:\.\d+)?)\s*%\s*of\s*(\d+(?:\.\d+)?)'
        match = re.search(percentage_pattern, expression.lower())
        
        if match:
            percentage = float(match.group(1))
            number = float(match.group(2))
            result = (percentage / 100) * number
            
            return f"Calculation: {percentage}% of {number} = {result:,.2f}\n\nSteps:\n1. Convert {percentage}% to decimal: {percentage}/100 = {percentage/100}\n2. Multiply: {percentage/100} × {number} = {result:,.2f}"
        
        # For simple arithmetic expressions
        # Security: only allow safe mathematical operations
        allowed_chars = set('0123456789+-*/()%. ')
        if not all(c in allowed_chars for c in expression):
            return f"Error: Invalid characters in expression. Only numbers and operators (+, -, *, /, %) are allowed.\n\nYou provided: '{expression}'\nTry something like: '2 + 2' or '10 * 5'"
        
        # Check for common syntax issues
        if expression.count('(') != expression.count(')'):
            return "Error: Unmatched parentheses in expression. Please check your brackets."
        
        # Evaluate the expression
        result = eval(expression, {"__builtins__": {}}, {})
        
        return f"Calculation: {expression} = {result}"
    
    except ZeroDivisionError:
        return f"Error: Division by zero is not allowed.\n\nYou tried to calculate: '{expression}'\nDivision by zero is mathematically undefined. Please use a non-zero divisor."
    except SyntaxError:
        return f"Error: Invalid mathematical expression syntax.\n\nYou provided: '{expression}'\nThis doesn't follow proper math syntax. Try examples like:\n  - '2 + 2'\n  - '10 * 5'\n  - '18% of 24500'\n  - '(5 + 3) * 2'"
    except ValueError as e:
        return f"Error: Invalid value in expression.\n\nDetails: {str(e)}\nPlease check your numbers and try again."
    except Exception as e:
        return f"Error calculating '{expression}': {str(e)}\n\nPlease check the expression format and try again."


# Mock FAQ Knowledge Base
FAQ_DATABASE = {
    "refund policy": {
        "answer": "Our refund policy allows returns within 30 days of purchase with original receipt.",
        "source_title": "Returns and Refunds Policy"
    },
    "shipping": {
        "answer": "We offer free shipping on orders over $50. Standard shipping takes 5-7 business days.",
        "source_title": "Shipping Information"
    },
    "business hours": {
        "answer": "Our customer support is available Monday-Friday, 9 AM - 5 PM EST.",
        "source_title": "Contact Information"
    },
    "payment methods": {
        "answer": "We accept Visa, MasterCard, American Express, PayPal, and Apple Pay.",
        "source_title": "Payment Options"
    },
    "warranty": {
        "answer": "All products come with a 1-year manufacturer warranty covering defects.",
        "source_title": "Warranty Information"
    }
}

def execute_lookup_faq(query: str) -> str:
    """
    Look up FAQ from mocked knowledge base.
    Returns fallback message when no match exists.
    """
    try:
        # Normalize query
        query_lower = query.lower().strip()
        
        # Search for matching FAQ
        for key, value in FAQ_DATABASE.items():
            if key in query_lower or query_lower in key:
                return json.dumps(value, indent=2)
        
        # Fallback message when no match
        available_topics = ", ".join(FAQ_DATABASE.keys())
        fallback = {
            "answer": f"I couldn't find an answer to '{query}' in our FAQ database.",
            "source_title": "No Match Found",
            "suggestion": f"Try asking about: {available_topics}"
        }
        return json.dumps(fallback, indent=2)
    
    except Exception as e:
        error_response = {
            "answer": f"Error searching FAQ: {str(e)}",
            "source_title": "Error"
        }
        return json.dumps(error_response, indent=2)