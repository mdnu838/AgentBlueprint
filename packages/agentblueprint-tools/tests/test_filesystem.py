import pytest
from pathlib import Path
from agentblueprint_tools.filesystem import FileWriteTool, FileReadTool

def test_file_write_normal(tmp_path):
    tool = FileWriteTool(base_dir=str(tmp_path))
    res = tool.run("test.txt", "hello")
    assert "Successfully" in res
    assert (tmp_path / "test.txt").read_text() == "hello"

def test_file_write_path_traversal_relative(tmp_path):
    tool = FileWriteTool(base_dir=str(tmp_path))
    res = tool.run("../outside.txt", "evil")
    assert "Access denied" in res
    assert "Path traversal detected" in res
    assert not (tmp_path.parent / "outside.txt").exists()

def test_file_write_path_traversal_absolute(tmp_path):
    tool = FileWriteTool(base_dir=str(tmp_path))
    absolute_outside_path = str(tmp_path.parent / "outside.txt")
    res = tool.run(absolute_outside_path, "evil")
    assert "Access denied" in res
    assert "Path traversal detected" in res
    assert not (tmp_path.parent / "outside.txt").exists()

def test_file_read_normal(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("world")

    tool = FileReadTool(base_dir=str(tmp_path))
    res = tool.run("test.txt")
    assert res == "world"

def test_file_read_path_traversal_relative(tmp_path):
    outside_file = tmp_path.parent / "my_secret_data.txt"
    # use content different from the filename itself to verify content isn't read
    outside_file.write_text("CONFIDENTIAL_CONTENT")

    tool = FileReadTool(base_dir=str(tmp_path))
    res = tool.run("../my_secret_data.txt")
    assert "Access denied" in res
    assert "Path traversal detected" in res
    assert "CONFIDENTIAL_CONTENT" not in res

def test_file_read_path_traversal_absolute(tmp_path):
    outside_file = tmp_path.parent / "my_secret_data.txt"
    outside_file.write_text("CONFIDENTIAL_CONTENT")

    tool = FileReadTool(base_dir=str(tmp_path))
    absolute_outside_path = str(outside_file)
    res = tool.run(absolute_outside_path)
    assert "Access denied" in res
    assert "Path traversal detected" in res
    assert "CONFIDENTIAL_CONTENT" not in res
