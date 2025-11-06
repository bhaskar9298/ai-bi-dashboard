"""
Test the exact error we're seeing
"""
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

print("Testing orchestration_agent.process_query() call...\n")

try:
    from agents.orchestration_agent import orchestration_agent
    
    print("Test 1: Call with positional argument (OLD WAY - SHOULD FAIL)")
    try:
        result = orchestration_agent.process_query("test query", "test_collection")
        print("   ✅ Succeeded (unexpected)")
    except TypeError as e:
        print(f"   ❌ Failed: {e}")
        print("   This is the error you're seeing!")
    
    print("\nTest 2: Call with keyword arguments (NEW WAY - SHOULD WORK)")
    try:
        result = orchestration_agent.process_query(
            query="test query",
            collection="test_collection"
        )
        print("   ✅ Succeeded!")
        print("   The fix is working, but you need to restart the server")
    except TypeError as e:
        print(f"   ❌ Still failing: {e}")
        print("   The cached bytecode is still being used!")
    except Exception as e:
        print(f"   ⚠️  Different error (OK): {type(e).__name__}: {e}")
        print("   This means the signature is correct, just other issues")

except Exception as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()
