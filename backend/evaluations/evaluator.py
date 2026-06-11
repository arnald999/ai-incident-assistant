import json
import time
import sys

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

DATASET_PATH = Path(__file__).parent / "golden_dataset.json"


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

    result = response.json()

    expected = test_case["expected"]

    severity_match = (
        result.get("severity") == expected["severity"]
    )

    tools_used = set(result.get("tools_used", []))
    required_tools = set(expected["required_tools"])

    tools_match = required_tools.issubset(tools_used)

    root_cause = result.get("root_cause", "")

    keyword_match_result = keyword_match(
        root_cause,
        expected["root_cause_keywords"],
    )

    passed = (
        severity_match
        and tools_match
        and keyword_match_result
    )

    return {
        "name": test_case["name"],
        "passed": passed,
        "latency_ms": duration_ms,
        "severity_match": severity_match,
        "tools_match": tools_match,
        "keyword_match": keyword_match_result,
        "actual_root_cause": root_cause,
    }


def main():
    with open(DATASET_PATH, "r") as f:
        dataset = json.load(f)

    results = []

    for test_case in dataset:
        results.append(evaluate_case(test_case))

    passed = sum(1 for r in results if r["passed"])

    print("\n=== Evaluation Report ===\n")

    for result in results:
        status = "PASS" if result["passed"] else "FAIL"

        print(
            f"[{status}] "
            f"{result['name']} "
            f"({result['latency_ms']}ms)"
        )

    print(
        f"\nAccuracy: "
        f"{passed}/{len(results)} "
        f"({round((passed / len(results)) * 100, 2)}%)"
    )


if __name__ == "__main__":
    main()