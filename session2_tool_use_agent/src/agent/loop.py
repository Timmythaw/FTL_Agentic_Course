# src/agent/loop.py
"""
Message-handling loop for the tool-using agent WITH STATE MANAGEMENT.
Implements the core loop: user prompt → model → tool selection → tool execution → final answer
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
from src.tools.schemas import TOOLS
from src.agent.state import AgentState, display_state
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ToolUsingAgent:
    """
    Agent that uses tools to answer user queries with state management.
    Implements the message-handling loop as required by Part B.3.
    Now includes state/memory for Part B.4.
    """
    
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        """
        Initialize the agent with Gemini model and tools.
        
        Args:
            model_name: The Gemini model to use (default: gemini-2.5-flash)
        """
        # Initialize the LLM
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        # Bind tools to the model
        self.llm_with_tools = self.llm.bind_tools(TOOLS)
        
        # Message history
        self.messages: List[Any] = []
        
        # State management (Part B.4)
        self.state = AgentState()
        
        print(f"Agent initialized with model: {model_name}")
        print(f"Tools bound: {[tool.name for tool in TOOLS]}")
        print(f"State management enabled")
    
    def run(self, user_input: str, verbose: bool = True) -> str:
        """
        Run the agent with a user query.
        Implements the message-handling loop with state management:
        1. Store user intent in state
        2. Add context from state to help with reference resolution
        3. User prompt → model
        4. Model selects tool + arguments
        5. Run tool and store result in state
        6. Send tool result back to model
        7. Print final answer
        
        Args:
            user_input: The user's question/request
            verbose: Whether to print intermediate steps
            
        Returns:
            The final answer from the agent
        """
        if verbose:
            print("\n" + "=" * 60)
            print(f"USER: {user_input}")
            print("=" * 60)
        
        # Part B.4: Store user intent
        self.state.add_user_intent(user_input)
        
        # Add system message with context if we have state
        if len(self.messages) == 0 and self.state.last_location:
            context_msg = SystemMessage(
                content=f"Context from previous conversation: {self.state.get_context_summary()}"
            )
            self.messages.append(context_msg)
        
        # Step 1: Add user message and invoke model
        self.messages.append(HumanMessage(content=user_input))
        
        if verbose:
            print("\n[STEP 1] Sending prompt to model...")
            if self.state.last_tool_name:
                print(f"[STATE] Context available: {self.state.get_context_summary()}")
        
        # Step 2: Model responds (may include tool calls)
        ai_message = self.llm_with_tools.invoke(self.messages)
        self.messages.append(ai_message)
        
        # Step 3: Check if model wants to use tools
        if ai_message.tool_calls:
            if verbose:
                print(f"\n[STEP 2] Model selected {len(ai_message.tool_calls)} tool(s):")
            
            # Execute each tool call
            for tool_call in ai_message.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_id = tool_call["id"]
                
                if verbose:
                    print(f"\n  → Tool: {tool_name}")
                    print(f"    Arguments: {tool_args}")
                
                # Step 4: Execute the tool
                tool_result = self._execute_tool(tool_name, tool_args)
                
                # Part B.4: Store tool result in state
                self.state.update_tool_result(tool_name, tool_args, tool_result)
                
                if verbose:
                    print(f"    Result: {tool_result[:100]}..." if len(tool_result) > 100 else f"    Result: {tool_result}")
                
                # Create tool message with result
                tool_message = ToolMessage(
                    content=tool_result,
                    tool_call_id=tool_id
                )
                self.messages.append(tool_message)
            
            # Step 5: Send tool results back to model for final answer
            if verbose:
                print(f"\n[STEP 3] Sending tool results back to model...")
            
            final_response = self.llm_with_tools.invoke(self.messages)
            self.messages.append(final_response)
            
            final_answer = final_response.content
        else:
            # No tools needed, use direct response
            final_answer = ai_message.content
        
        if verbose:
            print(f"\n[FINAL ANSWER]")
            print(f"AGENT: {final_answer}")
            print("=" * 60)
            
            # Display state after response
            display_state(self.state)
        
        return str(final_answer)
    
    def _execute_tool(self, tool_name: str, tool_args: Dict[str, Any]) -> str:
        """
        Execute a tool by name with given arguments.
        Handles reference resolution using state.
        
        Args:
            tool_name: Name of the tool to execute
            tool_args: Arguments to pass to the tool
            
        Returns:
            Tool execution result as string
        """
        # Part B.4: Reference resolution for "that" in location queries
        if tool_name == "get_time" and "location" in tool_args:
            location = tool_args["location"].lower()
            # If user says "convert that to UTC", use last location
            if location in ["that", "it", "there"] and self.state.last_location:
                print(f"    [STATE] Resolving '{location}' to last location: {self.state.last_location}")
                tool_args["location"] = self.state.last_location
        
        # Find the tool
        tool = None
        for t in TOOLS:
            if t.name == tool_name:
                tool = t
                break
        
        if tool is None:
            return f"Error: Tool '{tool_name}' not found"
        
        try:
            # Execute the tool with arguments
            result = tool.invoke(tool_args)
            return result
        except Exception as e:
            return f"Error executing {tool_name}: {str(e)}"
    
    def reset(self):
        """Clear message history but keep state for follow-up."""
        self.messages = []
        print("Message history cleared (state retained)")
    
    def reset_all(self):
        """Clear both message history and state."""
        self.messages = []
        self.state.reset()
        print("Message history and state cleared")


def demo_with_state():
    """
    Demo script showing agent with state management.
    Tests follow-up reference resolution as required by Part B.4.
    """
    print("\n" + "=" * 70)
    print("PART B.4: State Management Demo - Follow-up Reference Resolution")
    print("=" * 70)
    
    agent = ToolUsingAgent()
    
    # Test: Follow-up conversation (required by Part B.4)
    print("\n\n### FOLLOW-UP CONVERSATION TEST ###")
    print("Demonstrating: User asks about Cape Town, then 'Convert that to UTC'")
    
    # First query
    agent.run("What time is it in Cape Town?")
    
    # Follow-up query using reference "that"
    print("\n" + "-" * 70)
    print("NOW TESTING FOLLOW-UP WITH REFERENCE RESOLUTION...")
    print("-" * 70)
    agent.run("Convert that to UTC.")


if __name__ == "__main__":
    demo_with_state()