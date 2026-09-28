"""Invoice Period Router 的 Python 規則基準線。"""

from __future__ import annotations

import csv
from pathlib import Path


PERIOD_MAP = {
    "AA": "2026-01~02",
    "AB": "2026-01~02",
    "AC": "2026-01~02",
    "BA": "2026-03~04",
    "BB": "2026-03~04",
    "BC": "2026-03~04",
    "CA": "2026-05~06",
    "CB": "2026-05~06",
    "CC": "2026-05~06",
    "DA": "2026-07~08",
    "DB": "2026-07~08",
    "DC": "2026-07~08",
    "EA": "2026-09~10",
    "EB": "2026-09~10",
    "EC": "2026-09~10",
    "FA": "2026-11~12",
    "FB": "2026-11~12",
    "FC": "2026-11~12",
}


def invoice_period(invoice_no: str) -> str:
    """依發票格式與前兩碼回傳期別；格式錯誤或未知字軌回傳 UNKNOWN。"""
    if len(invoice_no) != 10:
        return "UNKNOWN"
    if not invoice_no[:2].isalpha() or not invoice_no[2:].isdigit():
        return "UNKNOWN"
    return PERIOD_MAP.get(invoice_no[:2].upper(), "UNKNOWN")


def main() -> None:
    project_dir = Path(__file__).parent
    input_path = project_dir / "test.csv"
    output_path = project_dir / "python_rule_results.csv"

    with input_path.open("r", encoding="utf-8-sig", newline="") as input_file:
        rows = list(csv.DictReader(input_file))

    correct = 0
    unknown_correct = 0
    unknown_total = 0
    for row in rows:
        prediction = invoice_period(row["invoice_no"])
        row["prediction"] = prediction
        row["correct"] = str(prediction == row["ground_truth"])
        correct += prediction == row["ground_truth"]
        if row["category"] == "unknown_prefix":
            unknown_total += 1
            unknown_correct += prediction == row["ground_truth"]

    fieldnames = [*rows[0].keys()]
    with output_path.open("w", encoding="utf-8", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"總筆數：{len(rows)}")
    print(f"整體準確率：{correct / len(rows):.2%}")
    print(f"未知字軌辨識率：{unknown_correct / unknown_total:.2%}")
    print(f"結果檔案：{output_path}")


if __name__ == "__main__":
    main()
