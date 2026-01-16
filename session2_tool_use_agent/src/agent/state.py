# src/agent/state.py
"""
State management for the agent.
Tracks memory across conversation turns for follow-up reference resolution.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AgentState:
    """
    Agent state that stores:
    - Last 3 user goals (or intents)
    - Last tool result
    - Last used location (if relevant)
    """
    
    # Last 3 user intents/goals
    user_intents: List[str] = field(default_factory=list)
    
    # Last tool that was called and its result
    last_tool_name: Optional[str] = None
    last_tool_result: Optional[str] = None
    last_tool_args: Optional[Dict[str, Any]] = None
    
    # Last used location (for time queries)
    last_location: Optional[str] = None
    
    # Timestamp of last interaction
    last_updated: Optional[datetime] = None
    
    def add_user_intent(self, intent: str):
        """
        Add a user intent and keep only the last 3.
        
        Args:
            intent: The user's question/request
        """
        self.user_intents.append(intent)
        # Keep only last 3
        if len(self.user_intents) > 3:
            self.user_intents = self.user_intents[-3:]
        self.last_updated = datetime.now()
    
    def update_tool_result(self, tool_name: str, tool_args: Dict[str, Any], result: str):
        """
        Update the last tool call information.
        
        Args:
            tool_name: Name of the tool that was called
            tool_args: Arguments passed to the tool
            result: Result returned by the tool
        """
        self.last_tool_name = tool_name
        self.last_tool_args = tool_args
        self.last_tool_result = result
        
        # Extract location if it was a get_time call
        if tool_name == "get_time" and "location" in tool_args:
            self.last_location = tool_args["location"]
        
        self.last_updated = datetime.now()
    
    def get_context_summary(self) -> str:
        """
        Get a summary of current state for context.
        
        Returns:
            A formatted string with state information
        """
        summary_parts = []
        
        if self.user_intents:
            summary_parts.append(f"Recent intents: {', '.join(self.user_intents)}")
        
        if self.last_tool_name:
            summary_parts.append(f"Last tool used: {self.last_tool_name}")
            if self.last_tool_args:
                summary_parts.append(f"Last tool args: {self.last_tool_args}")
        
        if self.last_location:
            summary_parts.append(f"Last location: {self.last_location}")
        
        return " | ".join(summary_parts) if summary_parts else "No context yet"
    
    def reset(self):
        """Clear all state."""
        self.user_intents = []
        self.last_tool_name = None
        self.last_tool_result = None
        self.last_tool_args = None
        self.last_location = None
        self.last_updated = None


def display_state(state: AgentState):
    """Pretty print the current state."""
    print("\n" + "=" * 60)
    print("CURRENT AGENT STATE (Memory)")
    print("=" * 60)
    print(f"Last 3 User Intents: {state.user_intents}")
    print(f"Last Tool: {state.last_tool_name}")
    print(f"Last Tool Args: {state.last_tool_args}")
    print(f"Last Tool Result: {state.last_tool_result[:80] + '...' if state.last_tool_result and len(state.last_tool_result) > 80 else state.last_tool_result}")
    print(f"Last Location: {state.last_location}")
    print(f"Last Updated: {state.last_updated}")
    print("=" * 60 + "\n")
