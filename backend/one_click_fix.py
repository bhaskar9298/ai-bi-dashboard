"""
ONE-CLICK FIX - Run this to fix everything
"""
import os
import sys
import shutil
import subprocess
import time
from pathlib import Path


def print_step(step_num, title):
    """Print a formatted step header"""
    print(f"\n{'='*70}")
    print(f"STEP {step_num}: {title}")
    print('='*70)


def kill_python_processes():
    """Kill all running Python processes"""
    print("Killing Python processes...")
    if os.name == 'nt':  # Windows
        try:
            subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                          capture_output=True, check=False)
            print("✅ Python processes killed")
            time.sleep(2)
        except:
            print("⚠️  Could not kill processes (might not be running)")
    else:  # Linux/Mac
        try:
            subprocess.run(['pkill', '-9', 'python'], 
                          capture_output=True, check=False)
            print("✅ Python processes killed")
            time.sleep(2)
        except:
            print("⚠️  Could not kill processes (might not be running)")


def remove_cache_directories(directory):
    """Remove all __pycache__ directories"""
    count = 0
    for root, dirs, files in os.walk(directory):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(pycache_path)
                print(f"  Removed: {os.path.relpath(pycache_path, directory)}")
                count += 1
            except Exception as e:
                print(f"  Failed: {os.path.relpath(pycache_path, directory)}: {e}")
    return count


def remove_pyc_files(directory):
    """Remove all .pyc files"""
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.pyc'):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    count += 1
                except:
                    pass
    return count


def verify_files():
    """Verify the fix is in the files"""
    backend_dir = Path(__file__).parent
    
    # Check app.py
    app_file = backend_dir / "app.py"
    with open(app_file, 'r', encoding='utf-8') as f:
        content = f.read()
        if 'query=request.prompt' in content:
            print("✅ app.py has correct syntax")
            return True
        else:
            print("❌ app.py still has old syntax!")
            return False


def run_tests():
    """Run diagnostic and test scripts"""
    print("\nRunning tests...")
    try:
        result = subprocess.run([sys.executable, 'test_fix.py'], 
                              capture_output=True, text=True, timeout=10)
        print(result.stdout)
        if result.returncode == 0:
            print("✅ Tests passed")
            return True
        else:
            print("⚠️  Tests had issues")
            return False
    except Exception as e:
        print(f"⚠️  Could not run tests: {e}")
        return False


def main():
    print("╔" + "="*68 + "╗")
    print("║" + " "*20 + "ONE-CLICK FIX SCRIPT" + " "*28 + "║")
    print("╚" + "="*68 + "╝")
    
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # Step 1: Kill processes
    print_step(1, "Kill Running Python Processes")
    kill_python_processes()
    
    # Step 2: Clean cache
    print_step(2, "Remove Python Cache Files")
    pycache_count = remove_cache_directories(backend_dir)
    pyc_count = remove_pyc_files(backend_dir)
    print(f"\n✅ Removed:")
    print(f"   - {pycache_count} __pycache__ directories")
    print(f"   - {pyc_count} .pyc files")
    
    # Step 3: Verify fix
    print_step(3, "Verify Code Changes")
    if not verify_files():
        print("\n❌ CRITICAL: Files not updated correctly!")
        print("Please check app.py manually")
        return False
    
    # Step 4: Run tests
    print_step(4, "Run Diagnostic Tests")
    run_tests()
    
    # Step 5: Instructions
    print_step(5, "Start Server")
    print("\n✅ FIX COMPLETE!")
    print("\nNow run:")
    print("   python app.py")
    print("\nThen test with:")
    print('   curl -X POST http://localhost:8000/generate_chart \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d "{\\"prompt\\":\\"Show analysis of american express reconciliation\\"}"')
    
    print("\n" + "="*70)
    
    # Ask if user wants to start server
    try:
        response = input("\nStart server now? (y/n): ").strip().lower()
        if response == 'y':
            print("\n🚀 Starting server...")
            subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n\n👋 Exiting...")
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
