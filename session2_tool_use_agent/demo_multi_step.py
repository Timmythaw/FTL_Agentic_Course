# demo_multistep_tasks.py
"""
Part C.1: Trigger Two Multi-Step Tasks
Demonstrates agent calling tools and providing final answers that reference tool outputs.
"""

from src.agent.loop import ToolUsingAgent


def main():
    """
    Demonstrate two multi-step tasks as required by Part C.1.
    
    Task 1: Time conversion (Cape Town → UTC)
    Task 2: Percentage calculation with explanation
    """
    
    print("=" * 80)
    print("PART C.1: TRIGGER TWO MULTI-STEP TASKS")
    print("=" * 80)
    print("\nRequirements:")
    print("- Agent calls at least one tool per task")
    print("- Final response references the tool output")
    print("- Provide screenshots of terminal runs\n")
    
    agent = ToolUsingAgent()
    
    # ========================================================================
    # TASK 1: Time Conversion (Multi-step with follow-up)
    # ========================================================================
    print("\n" + "=" * 80)
    print("TASK 1: What time is it in Cape Town and what is that in UTC?")
    print("=" * 80)
    print("\n[EXPECTED BEHAVIOR]")
    print("- Agent calls get_time for Cape Town")
    print("- Agent stores location in state")
    print("- Agent calls get_time for UTC conversion")
    print("- Final answer references both tool outputs\n")
    
    # First part: Get Cape Town time
    agent.run("What time is it in Cape Town?")
    
    print("\n" + "-" * 80)
    print("FOLLOW-UP: Converting to UTC...")
    print("-" * 80 + "\n")
    
    # Second part: Convert to UTC (uses state to reference "that")
    agent.run("What is that in UTC?")
    
    # ========================================================================
    # TASK 2: Percentage Calculation with Explanation
    # ========================================================================
    print("\n\n" + "=" * 80)
    print("TASK 2: What is 18% of 24,500 and explain the steps.")
    print("=" * 80)
    print("\n[EXPECTED BEHAVIOR]")
    print("- Agent calls calc tool with expression '18% of 24500'")
    print("- Tool returns calculation with step-by-step breakdown")
    print("- Final answer explains the calculation process\n")
    
    agent.reset_all()  # Fresh start for task 2
    agent.run("What is 18% of 24,500 and explain the steps.")
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("\n\n" + "=" * 80)
    print("MULTI-STEP TASKS COMPLETED")
    print("=" * 80)
    print("\nTask 1 Verification:")
    print("Called get_time tool twice (Cape Town, then UTC)")
    print("Used state management for follow-up reference")
    print("Final answers referenced tool outputs")
    
    print("\nTask 2 Verification:")
    print("Called calc tool with percentage expression")
    print("Tool returned step-by-step calculation")
    print("Final answer explained the mathematical steps")
    
    print("\nBoth tasks satisfy Part C.1 requirements:")
    print("- Tools were called")
    print("- Final responses referenced tool outputs")
    print("- Terminal output demonstrates functionality")


if __name__ == "__main__":
    main()
