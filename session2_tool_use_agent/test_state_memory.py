# test_state_memory.py
"""
Test script for Part B.4: State (Memory) Management
Demonstrates follow-up reference resolution
"""

from src.agent.loop import ToolUsingAgent


def main():
    """
    Test the agent's state management and follow-up resolution.
    Demonstrates the exact scenario from Part B.4:
    - User: "What time is it in Cape Town?"
    - User: "Convert that to UTC."
    """
    
    print("=" * 70)
    print("PART B.4: Testing State (Memory) Management")
    print("=" * 70)
    print("\nThis demonstrates:")
    print("- Storing last 3 user goals/intents")
    print("- Storing last tool result")
    print("- Storing last used location")
    print("- Follow-up reference resolution\n")
    
    # Initialize agent
    agent = ToolUsingAgent()
    
    print("\n" + "=" * 70)
    print("TEST: Follow-up Reference Resolution (Cape Town → UTC)")
    print("=" * 70)
    
    # First query - establishes context
    print("\n>>> First Query: Establishing context...")
    agent.run("What time is it in Cape Town?")
    
    # Second query - uses reference "that" which should resolve to "Cape Town"
    print("\n>>> Second Query: Using reference resolution...")
    agent.run("Convert that to UTC.")
    
    print("\n\n" + "=" * 70)
    print("Additional Test: Multiple Intents (tracks last 3)")
    print("=" * 70)
    
    agent.reset_all()
    
    agent.run("What's 10 + 5?")
    agent.reset()
    
    agent.run("What time is it in Bangkok?")
    agent.reset()
    
    agent.run("Tell me about shipping")
    agent.reset()
    
    agent.run("Calculate 25% of 1000")
    # State should now only show last 3 intents


if __name__ == "__main__":
    main()