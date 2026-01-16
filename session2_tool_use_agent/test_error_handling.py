# test_error_handling.py
"""
Test script for Part B.5: Error Handling and Recovery
Demonstrates clean error messages and retry capability
"""

from src.agent.loop import ToolUsingAgent


def test_error_scenarios():
    """
    Test various error scenarios:
    1. Invalid tool arguments (unsupported location)
    2. Tool failure (division by zero)
    3. Recovery and retry
    """
    
    print("=" * 70)
    print("PART B.5: Error Handling and Recovery")
    print("=" * 70)
    
    agent = ToolUsingAgent()
    
    # Error Test 1: Invalid location (tool argument error)
    print("\n\n" + "=" * 70)
    print("ERROR TEST 1: Invalid Location (Unsupported Tool Argument)")
    print("=" * 70)
    print("Testing: User asks for time in an unsupported location")
    print("Expected: Clean error message listing available locations\n")
    
    agent.run("What time is it in Mars?")
    
    # Show recovery - user can retry with valid location
    print("\n" + "-" * 70)
    print("RECOVERY: User retries with valid location")
    print("-" * 70)
    agent.reset()
    agent.run("What time is it in Tokyo?")
    
    # Error Test 2: Division by zero (tool execution failure)
    print("\n\n" + "=" * 70)
    print("ERROR TEST 2: Division by Zero (Tool Execution Failure)")
    print("=" * 70)
    print("Testing: User requests calculation that causes division by zero")
    print("Expected: Clean error message explaining the issue\n")
    
    agent.reset_all()
    agent.run("Calculate 100 divided by 0")
    
    # Show recovery - user can retry with valid expression
    print("\n" + "-" * 70)
    print("RECOVERY: User retries with valid calculation")
    print("-" * 70)
    agent.reset()
    agent.run("Calculate 100 divided by 5")
    
    # Error Test 3: Invalid mathematical expression
    print("\n\n" + "=" * 70)
    print("ERROR TEST 3: Invalid Expression Syntax")
    print("=" * 70)
    print("Testing: User provides malformed mathematical expression")
    print("Expected: Clean syntax error message\n")
    
    agent.reset_all()
    agent.run("Calculate 2 + + 3")
    
    # Show recovery
    print("\n" + "-" * 70)
    print("RECOVERY: User retries with correct syntax")
    print("-" * 70)
    agent.reset()
    agent.run("Calculate 2 + 3")
    
    # Error Test 4: FAQ not found (graceful fallback)
    print("\n\n" + "=" * 70)
    print("ERROR TEST 4: FAQ Query Not Found (Graceful Fallback)")
    print("=" * 70)
    print("Testing: User asks about topic not in FAQ database")
    print("Expected: Helpful fallback message with available topics\n")
    
    agent.reset_all()
    agent.run("What is your cryptocurrency policy?")
    
    # Show recovery
    print("\n" + "-" * 70)
    print("RECOVERY: User asks about available topic")
    print("-" * 70)
    agent.reset()
    agent.run("What is your warranty policy?")
    
    print("\n\n" + "=" * 70)
    print("ERROR HANDLING TESTS COMPLETED")
    print("=" * 70)
    print("\nKey Demonstrations:")
    print("✓ Invalid tool arguments return clean error messages")
    print("✓ Tool failures (division by zero, syntax errors) are caught")
    print("✓ Fallback messages are helpful and informative")
    print("✓ Agent allows retry after errors")
    print("✓ Conversation continues normally after recovery")


def test_model_invalid_args():
    """
    Additional test: Model provides invalid argument format
    """
    print("\n\n" + "=" * 70)
    print("BONUS TEST: Model Provides Unexpected Argument Format")
    print("=" * 70)
    
    agent = ToolUsingAgent()
    
    # This might cause the model to struggle with format
    agent.run("What time is it in 12345?")  # Non-location input
    
    agent.reset()
    agent.run("Calculate hello world")  # Non-math input


if __name__ == "__main__":
    test_error_scenarios()
    test_model_invalid_args()