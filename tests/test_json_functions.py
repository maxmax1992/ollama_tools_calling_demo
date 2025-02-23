import json
import os
import pytest
from structured_assistant.utils import add_to_json_file, clean_json_file

def test_add_to_json_file_no_exists():
    clean_json_file()  # Clean up before test
    add_to_json_file({"title": "test", "description": "test", "severity": 1})
    with open("issues.json", "r") as f:
        issues = json.load(f)
    assert len(issues) == 1
    assert issues[0]["title"] == "test"
    assert issues[0]["description"] == "test"
    assert issues[0]["severity"] == 1

def test_append_new_issue_to_file_with_existing_issues():
    clean_json_file()  # Clean up before test
    add_to_json_file({"title": "test", "description": "test", "severity": 1})
    add_to_json_file({"title": "test2", "description": "test2", "severity": 2})
    with open("issues.json", "r") as f:
        issues = json.load(f)
    assert len(issues) == 2
    assert issues[0]["title"] == "test"
    assert issues[1]["title"] == "test2"
    clean_json_file()  # Clean up after test 