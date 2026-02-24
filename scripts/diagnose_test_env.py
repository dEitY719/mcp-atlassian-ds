#!/usr/bin/env python3
"""
Test environment diagnosis script.

내부 PC에서 테스트 실패 원인을 진단하기 위한 스크립트입니다.
이 스크립트를 실행하고 출력 결과를 외부 Claude와 공유하세요.
"""

import sys
import json
from pathlib import Path
from typing import Any


def check_python_version() -> dict[str, Any]:
    """Check Python version."""
    return {
        "python_version": sys.version,
        "python_executable": sys.executable,
    }


def check_jira_constants() -> dict[str, Any]:
    """Check Jira constants configuration."""
    try:
        from src.mcp_atlassian.jira.constants import DEFAULT_READ_JIRA_FIELDS

        return {
            "DEFAULT_READ_JIRA_FIELDS": sorted(list(DEFAULT_READ_JIRA_FIELDS)),
            "field_count": len(DEFAULT_READ_JIRA_FIELDS),
            "field_types": list(set(type(f).__name__ for f in DEFAULT_READ_JIRA_FIELDS)),
        }
    except ImportError as e:
        return {"error": f"Failed to import: {e}"}


def check_other_constants() -> dict[str, Any]:
    """Check Confluence and other constants."""
    try:
        from src.mcp_atlassian.confluence.constants import DEFAULT_READ_CONFLUENCE_FIELDS
        from src.mcp_atlassian.models.constants import DEFAULT_FIELD_MAPPINGS

        return {
            "confluence_fields_count": len(DEFAULT_READ_CONFLUENCE_FIELDS),
            "confluence_fields": sorted(list(DEFAULT_READ_CONFLUENCE_FIELDS)),
            "field_mappings_count": len(DEFAULT_FIELD_MAPPINGS),
        }
    except ImportError as e:
        return {"error": f"Failed to import: {e}"}


def check_test_expectations() -> dict[str, Any]:
    """Check what tests expect."""
    return {
        "jira_fields_expected_count": 10,
        "jira_expected_fields": {
            "summary",
            "description",
            "status",
            "assignee",
            "reporter",
            "labels",
            "priority",
            "created",
            "updated",
            "issuetype",
        },
        "note": "Test expects 10 fields, but constants may have more (comment field added?)",
    }


def check_test_failures() -> dict[str, Any]:
    """Run specific test and capture output."""
    import subprocess

    result = subprocess.run(
        ["python", "-m", "pytest", "tests/unit/jira/test_constants.py::TestDefaultReadJiraFields::test_type_and_structure", "-v"],
        capture_output=True,
        text=True,
    )

    return {
        "return_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def main() -> None:
    """Run all diagnostics."""
    diagnostics = {
        "environment": check_python_version(),
        "jira_constants": check_jira_constants(),
        "other_constants": check_other_constants(),
        "test_expectations": check_test_expectations(),
        "test_results": check_test_failures(),
    }

    print("=" * 80)
    print("TEST ENVIRONMENT DIAGNOSIS")
    print("=" * 80)
    print(json.dumps(diagnostics, indent=2, default=str))
    print("=" * 80)
    print("\n[공유할 정보]")
    print("1. jira_constants.DEFAULT_READ_JIRA_FIELDS 현재 필드:")
    if "DEFAULT_READ_JIRA_FIELDS" in diagnostics["jira_constants"]:
        for field in diagnostics["jira_constants"]["DEFAULT_READ_JIRA_FIELDS"]:
            print(f"   - {field}")
    print(f"\n2. 필드 개수: {diagnostics['jira_constants'].get('field_count', 'N/A')}")
    print(f"3. 테스트 기대값: {diagnostics['test_expectations']['jira_fields_expected_count']}")


if __name__ == "__main__":
    main()
