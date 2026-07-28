import pytest
import os
from pathlib import Path
from agentblueprint_tools.filesystem import FileReadTool, FileWriteTool

def test_file_read_tool_normal(tmp_path):
    tool = FileReadTool(base_dir=str(tmp_path))
    file_path = tmp_path / "test.txt"
    file_path.write_text("hello world")

    result = tool.run("test.txt")
    assert result == "hello world"

def test_file_read_tool_traversal(tmp_path):
    tool = FileReadTool(base_dir=str(tmp_path))

    # Try reading outside the base_dir
    parent_file = tmp_path.parent / "secret.txt"
    parent_file.write_text("secret")

    result = tool.run("../secret.txt")
    assert "Access denied" in result

    # Clean up
    parent_file.unlink()

def test_file_read_tool_absolute_path_traversal(tmp_path):
    tool = FileReadTool(base_dir=str(tmp_path))

    # Try reading an absolute path outside base_dir
    parent_file = tmp_path.parent / "secret2.txt"
    parent_file.write_text("secret")

    result = tool.run(str(parent_file))
    assert "Access denied" in result

    # Clean up
    parent_file.unlink()

def test_file_write_tool_normal(tmp_path):
    tool = FileWriteTool(base_dir=str(tmp_path))

    result = tool.run("out.txt", "some content")
    assert "Successfully wrote" in result

    assert (tmp_path / "out.txt").read_text() == "some content"

def test_file_write_tool_traversal(tmp_path):
    tool = FileWriteTool(base_dir=str(tmp_path))

    result = tool.run("../out2.txt", "some content")
    assert "Access denied" in result

    assert not (tmp_path.parent / "out2.txt").exists()

def test_file_write_tool_absolute_path_traversal(tmp_path):
    tool = FileWriteTool(base_dir=str(tmp_path))

    abs_path_out = tmp_path.parent / "out3.txt"
    result = tool.run(str(abs_path_out), "some content")
    assert "Access denied" in result

    assert not abs_path_out.exists()
