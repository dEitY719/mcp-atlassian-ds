#!/usr/bin/env python3
"""
Comprehensive test environment diagnosis script.

회사 내부 PC에서 실행하여 테스트 환경의 모든 정보를 수집합니다.
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime


class DiagnosticCollector:
    """Collect comprehensive diagnostic information."""

    def __init__(self):
        self.results = {}
        self.timestamp = datetime.now().isoformat()

    def section(self, name: str):
        """Print and track section."""
        print(f"\n{'=' * 80}")
        print(f"[{name}]")
        print('=' * 80)

    def run_command(self, cmd: list, section_name: str) -> dict:
        """Run command and capture output."""
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return {
                "success": True,
                "return_code": result.returncode,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip() if result.stderr else None,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def diagnose_environment(self):
        """1. Diagnose Python environment."""
        self.section("1. Python 환경")

        env_info = {
            "timestamp": self.timestamp,
            "python_version": sys.version,
            "python_executable": sys.executable,
            "python_version_info": {
                "major": sys.version_info.major,
                "minor": sys.version_info.minor,
                "micro": sys.version_info.micro,
            },
        }

        # Check installed packages
        result = self.run_command(
            ["pip", "list", "--format=json"],
            "pip_list"
        )

        if result["success"]:
            try:
                packages = json.loads(result["stdout"])
                key_packages = {
                    p["name"]: p["version"]
                    for p in packages
                    if p["name"] in ["pytest", "fastapi", "pydantic", "sqlalchemy", "httpx"]
                }
                env_info["key_packages"] = key_packages
            except:
                pass

        print(json.dumps(env_info, indent=2))
        self.results["environment"] = env_info
        return env_info

    def diagnose_constants(self):
        """2. Diagnose constants values."""
        self.section("2. 상수 값 확인")

        constants_info = {}

        # Jira constants
        try:
            from src.mcp_atlassian.jira.constants import DEFAULT_READ_JIRA_FIELDS

            jira_info = {
                "fields": sorted(list(DEFAULT_READ_JIRA_FIELDS)),
                "field_count": len(DEFAULT_READ_JIRA_FIELDS),
                "field_types": list(set(type(f).__name__ for f in DEFAULT_READ_JIRA_FIELDS)),
                "is_set": isinstance(DEFAULT_READ_JIRA_FIELDS, set),
            }
            constants_info["jira"] = jira_info
            print(f"\n✓ Jira Fields (개수: {jira_info['field_count']}):")
            for field in jira_info["fields"]:
                print(f"  - {field}")
        except Exception as e:
            constants_info["jira"] = {"error": str(e)}
            print(f"✗ Jira: {e}")

        # Confluence constants
        try:
            from src.mcp_atlassian.confluence.constants import (
                DEFAULT_READ_CONFLUENCE_FIELDS,
            )

            conf_info = {
                "fields": sorted(list(DEFAULT_READ_CONFLUENCE_FIELDS)),
                "field_count": len(DEFAULT_READ_CONFLUENCE_FIELDS),
            }
            constants_info["confluence"] = conf_info
            print(f"\n✓ Confluence Fields (개수: {conf_info['field_count']}):")
            for field in conf_info["fields"]:
                print(f"  - {field}")
        except Exception as e:
            constants_info["confluence"] = {"error": str(e)}
            print(f"✗ Confluence: {e}")

        # Models constants
        try:
            from src.mcp_atlassian.models.constants import DEFAULT_FIELD_MAPPINGS

            models_info = {
                "field_mappings_count": len(DEFAULT_FIELD_MAPPINGS),
                "mappings_keys": list(DEFAULT_FIELD_MAPPINGS.keys()),
            }
            constants_info["models"] = models_info
            print(f"\n✓ Field Mappings (개수: {models_info['field_mappings_count']})")
        except Exception as e:
            constants_info["models"] = {"error": str(e)}
            print(f"✗ Models: {e}")

        self.results["constants"] = constants_info
        return constants_info

    def diagnose_test_expectations(self):
        """3. Check test expectations."""
        self.section("3. 테스트 기대값")

        expectations = {
            "jira_fields_expected_count": 10,
            "jira_expected_fields": sorted([
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
            ]),
        }

        print(f"기대 필드 개수: {expectations['jira_fields_expected_count']}")
        print("기대 필드:")
        for field in expectations["jira_expected_fields"]:
            print(f"  - {field}")

        self.results["test_expectations"] = expectations
        return expectations

    def diagnose_specific_test(self):
        """4. Run specific failing test."""
        self.section("4. test_type_and_structure 실행 결과")

        result = self.run_command(
            [
                "python", "-m", "pytest",
                "tests/unit/jira/test_constants.py::TestDefaultReadJiraFields::test_type_and_structure",
                "-v", "--tb=short"
            ],
            "specific_test"
        )

        print(result["stdout"])
        if result["stderr"]:
            print("STDERR:", result["stderr"])

        self.results["specific_test"] = result
        return result

    def diagnose_all_jira_tests(self):
        """5. Run all Jira constant tests."""
        self.section("5. 전체 Jira 상수 테스트 결과")

        result = self.run_command(
            [
                "python", "-m", "pytest",
                "tests/unit/jira/test_constants.py",
                "-v", "--tb=short"
            ],
            "jira_tests"
        )

        print(result["stdout"])
        if result["stderr"]:
            print("STDERR:", result["stderr"])

        self.results["jira_tests"] = result
        return result

    def diagnose_all_tests(self):
        """6. Run all tests."""
        self.section("6. 전체 테스트 요약")

        result = self.run_command(
            ["python", "-m", "pytest", "tests/", "-q", "--tb=no"],
            "all_tests"
        )

        # Extract summary
        lines = result["stdout"].split("\n")
        summary_lines = [l for l in lines if "passed" in l or "failed" in l or "error" in l]

        print(result["stdout"][-500:] if len(result["stdout"]) > 500 else result["stdout"])

        self.results["all_tests_summary"] = {
            "return_code": result["return_code"],
            "summary": summary_lines,
        }
        return result

    def generate_report(self):
        """Generate JSON report."""
        self.section("📊 진단 리포트 (JSON)")

        report_path = Path("diagnose_report.json")
        with open(report_path, "w") as f:
            json.dump(self.results, f, indent=2, default=str)

        print(f"✓ 리포트 저장됨: {report_path}")
        print("\n전체 리포트 내용:")
        print(json.dumps(self.results, indent=2, default=str))

    def generate_summary(self):
        """Generate human-readable summary."""
        self.section("📋 요약 & 다음 단계")

        jira_count = self.results.get("constants", {}).get("jira", {}).get("field_count")
        expected_count = self.results.get("test_expectations", {}).get("jira_fields_expected_count")

        print(f"""
[현재 상태]
- Jira 필드 개수: {jira_count} (기대값: {expected_count})
- 차이: {jira_count - expected_count if jira_count and expected_count else 'N/A'} 개

[권장 해결 방안]
1. test_type_and_structure 테스트 파일 확인
   → tests/unit/jira/test_constants.py 16번 줄

2. 두 가지 선택지:
   A. 테스트 수정: assert len(...) == {jira_count}
   B. 상수 수정: comment 필드 제거

[커뮤니케이션]
이 리포트를 외부 Claude와 공유하세요:
- diagnose_report.json (전체 데이터)
- 또는 위 출력 결과 복사
""")

    def run_all(self):
        """Run all diagnostics."""
        print("\n🔍 MCP Atlassian 테스트 환경 진단 시작")
        print(f"시작 시간: {self.timestamp}")

        try:
            self.diagnose_environment()
            self.diagnose_constants()
            self.diagnose_test_expectations()
            self.diagnose_specific_test()
            self.diagnose_all_jira_tests()
            self.diagnose_all_tests()
            self.generate_report()
            self.generate_summary()
        except Exception as e:
            print(f"\n❌ 진단 중 오류 발생: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    collector = DiagnosticCollector()
    collector.run_all()
