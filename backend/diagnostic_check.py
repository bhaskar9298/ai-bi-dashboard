"""
Diagnostic script to check the actual loaded method signature
"""
import sys
import inspect
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

print("="*70)
print("🔍 DIAGNOSTIC CHECK")
print("="*70)

try:
    # Import the orchestration agent
    from agents.orchestration_agent import orchestration_agent, OrchestrationAgent
    
    print("\n✅ Successfully imported orchestration_agent")
    
    # Check the class
    print(f"\n📦 Class: {OrchestrationAgent}")
    print(f"   Type: {type(orchestration_agent)}")
    print(f"   Instance of OrchestrationAgent: {isinstance(orchestration_agent, OrchestrationAgent)}")
    
    # Get the process_query method
    process_query_method = orchestration_agent.process_query
    print(f"\n🔧 Method: {process_query_method}")
    
    # Inspect the signature
    sig = inspect.signature(process_query_method)
    print(f"\n📋 Method Signature:")
    print(f"   {process_query_method.__name__}{sig}")
    
    # Get parameters
    print(f"\n📝 Parameters:")
    for param_name, param in sig.parameters.items():
        print(f"   - {param_name}: {param.annotation if param.annotation != inspect.Parameter.empty else 'no annotation'}")
        if param.default != inspect.Parameter.empty:
            print(f"     Default: {param.default}")
    
    # Test calling it
    print(f"\n🧪 Testing method call...")
    print(f"   Calling with: query='test', collection=None")
    
    try:
        # This should work
        result = orchestration_agent.process_query(query="test query", collection=None)
        print(f"   ✅ Call succeeded (expected - MongoDB might fail but call signature is correct)")
    except TypeError as e:
        print(f"   ❌ Call failed with TypeError: {e}")
        print(f"   This indicates the signature is still wrong!")
    except Exception as e:
        print(f"   ⚠️  Call failed with: {type(e).__name__}: {e}")
        print(f"   This is OK - it's not a signature issue")
    
    # Check the source file location
    import agents.orchestration_agent as orch_module
    print(f"\n📁 Source File:")
    print(f"   {orch_module.__file__}")
    
    # Check if there's a cached version
    if orch_module.__file__.endswith('.pyc'):
        print(f"   ⚠️  Loading from compiled bytecode!")
    else:
        print(f"   ✅ Loading from source .py file")

except Exception as e:
    print(f"\n❌ Error during import: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("END DIAGNOSTIC")
print("="*70)
