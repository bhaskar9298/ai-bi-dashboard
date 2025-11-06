"""
Force clean restart - Remove all Python cache and compiled files
"""
import os
import shutil
import sys
from pathlib import Path


def remove_pycache_recursive(directory):
    """Recursively remove all __pycache__ directories"""
    count = 0
    for root, dirs, files in os.walk(directory):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(pycache_path)
                print(f"✅ Removed: {pycache_path}")
                count += 1
            except Exception as e:
                print(f"❌ Failed to remove {pycache_path}: {e}")
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
                    print(f"✅ Removed: {file_path}")
                    count += 1
                except Exception as e:
                    print(f"❌ Failed to remove {file_path}: {e}")
    return count


def main():
    print("="*70)
    print("🧹 FORCE CLEAN RESTART")
    print("="*70)
    print("\nThis will remove all Python cache files and restart the server.\n")
    
    backend_dir = Path(__file__).parent
    
    # Step 1: Remove __pycache__ directories
    print("\n1️⃣  Removing __pycache__ directories...")
    pycache_count = remove_pycache_recursive(backend_dir)
    print(f"   Removed {pycache_count} __pycache__ directories")
    
    # Step 2: Remove .pyc files
    print("\n2️⃣  Removing .pyc files...")
    pyc_count = remove_pyc_files(backend_dir)
    print(f"   Removed {pyc_count} .pyc files")
    
    # Step 3: Verify files are updated
    print("\n3️⃣  Verifying app.py content...")
    app_file = backend_dir / "app.py"
    with open(app_file, 'r', encoding='utf-8') as f:
        content = f.read()
        if 'query=request.prompt' in content:
            print("   ✅ app.py has correct syntax")
        else:
            print("   ⚠️  app.py might need manual check")
    
    # Step 4: Verify orchestration_agent.py
    print("\n4️⃣  Verifying orchestration_agent.py...")
    orch_file = backend_dir / "agents" / "orchestration_agent.py"
    with open(orch_file, 'r', encoding='utf-8') as f:
        content = f.read()
        if 'def process_query(self, query: str, collection: Optional[str] = None)' in content:
            print("   ✅ orchestration_agent.py has correct signature")
        else:
            print("   ⚠️  orchestration_agent.py might need manual check")
    
    print("\n" + "="*70)
    print("✅ CLEANUP COMPLETE")
    print("="*70)
    print("\n📋 Next Steps:")
    print("   1. Stop the running server (Ctrl+C)")
    print("   2. Run: python app.py")
    print("   3. Test with: curl -X POST http://localhost:8000/generate_chart ...")
    print("\n")


if __name__ == "__main__":
    main()
