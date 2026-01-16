# test_tools_direct.py (in the root directory)
"""
Direct testing of tool execution logic.
This demonstrates calling each tool directly before integrating with LLM.
"""

from src.tools.execution import execute_get_time, execute_calc, execute_lookup_faq


def test_all_tools():
    print("=" * 60)
    print("PART B.2: Testing Tool Execution Logic")
    print("=" * 60)
    
    # Test 1: get_time
    print("\n1. Testing get_time tool:")
    print("-" * 40)
    locations = ["Cape Town", "New York", "Bangkok", "InvalidCity"]
    for loc in locations:
        result = execute_get_time(loc)
        print(f"Location: {loc}")
        print(f"Result: {result}\n")
    
    # Test 2: calc
    print("\n2. Testing calc tool:")
    print("-" * 40)
    expressions = [
        "18% of 24500",
        "2 + 2 * 3",
        "100 / 0",  # Error case
        "invalid$expression",  # Error case
    ]
    for expr in expressions:
        result = execute_calc(expr)
        print(f"Expression: {expr}")
        print(f"Result: {result}\n")
    
    # Test 3: lookup_faq
    print("\n3. Testing lookup_faq tool:")
    print("-" * 40)
    queries = [
        "refund policy",
        "shipping information",
        "how do I contact support",  # No direct match
        "unknown topic",  # Fallback case
    ]
    for query in queries:
        result = execute_lookup_faq(query)
        print(f"Query: {query}")
        print(f"Result: {result}\n")


if __name__ == "__main__":
    test_all_tools()
