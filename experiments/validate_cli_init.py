"""
Validation script for ab init command.
"""
import shutil
import subprocess
import sys
from pathlib import Path

def test_init_command():
    print("\n🧪 Testing ab init...")
    
    project_name = "test_project_gen"
    if Path(project_name).exists():
        shutil.rmtree(project_name)
        
    # Run init command via ab
    result = subprocess.run(
        ["uv", "run", "ab", "init", project_name],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"❌ Init failed: {result.stderr}")
        raise AssertionError("Init command failed")
        
    # Verify files
    expected_files = [
        "pyproject.toml",
        "README.md",
        "workflow.yaml",
        ".env.example",
        ".gitignore",
        f"src/{project_name}/main.py",
        f"src/{project_name}/__init__.py"
    ]
    
    base_path = Path(project_name)
    for f in expected_files:
        p = base_path / f
        if not p.exists():
            raise AssertionError(f"Missing file: {p}")
            
    print("✅ Project structure created successfully")
    
    # Cleanup
    shutil.rmtree(project_name)
    print("✅ Cleanup successful")

if __name__ == "__main__":
    try:
        test_init_command()
        print("\n✅ All validations passed!")
    except Exception as e:
        print(f"\n❌ Validation failed: {e}")
        sys.exit(1)
