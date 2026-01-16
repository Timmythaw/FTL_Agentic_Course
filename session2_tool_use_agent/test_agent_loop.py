# test_agent_loop.py
"""
Test script for Part B.3: Message-handling loop
"""

from src.agent.loop import ToolUsingAgent


def main():
    """Test the message-handling loop with various queries."""
    
    print("=" * 70)
    print("PART B.3: Testing Message-Handling Loop")
    print("=" * 70)
    
    # Initialize agent
    agent = ToolUsingAgent()
    
    # Test queries
    test_queries = [
        "What time is it in Bangkok?",
        "Calculate 25 * 48",
        "Tell me about your shipping policy",
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n\n{'='*70}")
        print(f"TEST {i}/{len(test_queries)}")
        print(f"{'='*70}")
        agent.run(query)
        agent.reset()


if __name__ == "__main__":
    main()
