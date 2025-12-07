"""
Validation script for 'ab docker' command.
"""
from pathlib import Path
import subprocess
import shutil

def test_docker_command():
    print("\n🧪 Testing 'ab docker'...")
    
    # We need to simulate running inside a project
    temp_dir = Path("temp_docker_test")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()
    
    try:
        # We can't easily switch CWD for the current process safely in this context
        # So we'll mock the Path behavior or just run the CLI subprocess
        
        cmd = ["uv", "run", "ab", "docker"]
        result = subprocess.run(cmd, cwd=temp_dir, capture_output=True, text=True)
        
        print(result.stdout)
        
        dockerfile = temp_dir / "Dockerfile"
        dockerignore = temp_dir / ".dockerignore"
        
        assert dockerfile.exists()
        assert dockerignore.exists()
        assert "FROM python:3.11-slim" in dockerfile.read_text()
        
        print("✅ Docker command validation successful")
        
    finally:
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    test_docker_command()
