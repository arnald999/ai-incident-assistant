import json
import sys
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

DATASET_PATH = Path(__file__).parent / "golden_dataset.json"
REPORT_DIR = Path(__file__).parent / "reports"
REPORT_PATH = REPORT_DIR / "latest_report.json"


def keyword_match(text: str, keywords: list[str]) -> bool:
    text = text.lower()
    return all(keyword.lower() in text for keyword in keywords)


def evaluate_case(test_case: dict) -> dict:
    start_time = time.time()

    response = client.post(
        "/api/alerts/analyze",
        json=test_case["alert"],
    )

    duration_ms = round((time.time() - start_time) * 1000, 2)

    if response.status_code != 200:
        return {
            "name": test_case["name"],
            "passed": False,
            "latency_ms": duration_ms,
            "severity_match": False,
            "tools_match": False,
            "keyword_match": False,
            "actual_root_cause": "",
            "error": response.text,
        }

    result = response.json()
    expected = test_case["expected"]

    severity_match = result.get("severity") == expected["severity"]

    tools_used = set(result.get("tools_used", []))
    required_tools = set(expected["required_tools"])
    tools_match = required_tools.issubset(tools_used)

    root_cause = result.get("root_cause", "")

    keyword_match_result = keyword_match(
        root_cause,
        expected["root_cause_keywords"],
    )

    passed = severity_match and tools_match and keyword_match_result

    return {
        "name": test_case["name"],
        "passed": passed,
        "latency_ms": duration_ms,
        "severity_match": severity_match,
        "tools_match": tools_match,
        "keyword_match": keyword_match_result,
        "expected_severity": expected["severity"],
        "actual_severity": result.get("severity"),
        "expected_tools": expected["required_tools"],
        "actual_tools": result.get("tools_used", []),
        "expected_keywords": expected["root_cause_keywords"],
        "actual_root_cause": root_cause,
    }


def save_report(results: list[dict]) -> None:
    REPORT_DIR.mkdir(exist_ok=True)

    passed_count = sum(1 for result in results if result["passed"])
    total_cases = len(results)

    report = {
        "total_cases": total_cases,
        "passed": passed_count,
        "failed": total_cases - passed_count,
        "accuracy": round((passed_count / total_cases) * 100, 2)
        if total_cases > 0
        else 0,
        "results": results,
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"\nReport saved to: {REPORT_PATH}")


def main() -> None:
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    results = []

    for test_case in dataset:
        results.append(evaluate_case(test_case))

    passed_count = sum(1 for result in results if result["passed"])
    total_cases = len(results)

    print("\n=== Evaluation Report ===\n")

    for result in results:
        status = "PASS" if result["passed"] else "FAIL"

        print(
            f"[{status}] "
            f"{result['name']} "
            f"({result['latency_ms']}ms)"
        )

        if not result["passed"]:
            print(f"  Severity match: {result['severity_match']}")
            print(f"  Tools match: {result['tools_match']}")
            print(f"  Keyword match: {result['keyword_match']}")
            print(f"  Actual root cause: {result['actual_root_cause']}")

    accuracy = (
        round((passed_count / total_cases) * 100, 2)
        if total_cases > 0
        else 0
    )

    print(
        f"\nAccuracy: "
        f"{passed_count}/{total_cases} "
        f"({accuracy}%)"
    )

    save_report(results)


if __name__ == "__main__":
    main()