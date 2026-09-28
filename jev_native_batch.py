#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""讀取 test.csv，批次呼叫 TypeSafe 原生 Jev API。"""

from __future__ import annotations

import csv
import json
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv


BASE_URL = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-latest"
PROJECT_DIR = Path(__file__).parent
DATA_FILE = PROJECT_DIR / "test.csv"
RESULT_FILE = PROJECT_DIR / "jev_native_results.json"


def load_api_key() -> str | None:
    """讀取發票路由器專案計劃目錄內的 API Key。"""
    load_dotenv(PROJECT_DIR / ".env", override=True)
    key = os.getenv("TYPESAFE_API_KEY")
    return key.strip().strip("'\"") if key else None


def build_payload(invoice_no: str) -> dict:
    return {
        "model": MODEL,
        "state": f"發票號碼：{invoice_no}",
        "questions": {
            "period": {
                "type": "choice",
                "instructions": "只根據發票號碼判斷所屬期別。請忽略後八碼流水號；未知字軌必須選 UNKNOWN。",
                "criteria": {
                    "2026-01~02": "前兩碼為 AA、AB 或 AC",
                    "2026-03~04": "前兩碼為 BA、BB 或 BC",
                    "2026-05~06": "前兩碼為 CA、CB 或 CC",
                    "2026-07~08": "前兩碼為 DA、DB 或 DC",
                    "2026-09~10": "前兩碼為 EA、EB 或 EC",
                    "2026-11~12": "前兩碼為 FA、FB 或 FC",
                    "UNKNOWN": "前兩碼不在上述字軌，或發票格式不符合 2 位英文字母加 8 位數字",
                },
            }
        },
    }


def run_one(session: requests.Session, api_key: str, row: dict) -> dict:
    started = time.perf_counter()
    response = session.post(
        BASE_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=build_payload(row["invoice_no"]),
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    answer = data.get("answers", {}).get("period", {})
    prediction = answer.get("choice")
    usage = data.get("usage", {})
    return {
        "id": row["id"],
        "invoice_no": row["invoice_no"],
        "ground_truth": row["ground_truth"],
        "prediction": prediction,
        "correct": prediction == row["ground_truth"],
        "confidence": answer.get("confidence"),
        "probabilities": answer.get("probabilities"),
        "elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
        "input_tokens": usage.get("input_tokens", 0),
        "output_tokens": usage.get("output_tokens", 0),
        "status": "success",
    }


def main() -> int:
    api_key = load_api_key()
    if not api_key:
        print("找不到 TYPESAFE_API_KEY，請設定發票路由器專案計劃/.env。")
        return 1

    with DATA_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))

    results, failures = [], []
    started = time.perf_counter()
    with requests.Session() as session:
        for index, row in enumerate(rows, 1):
            try:
                result = run_one(session, api_key, row)
                results.append(result)
                print(f"[{index}/{len(rows)}] {row['invoice_no']} → {result['prediction']}")
            except (requests.RequestException, ValueError, KeyError) as exc:
                failures.append({"id": row.get("id"), "invoice_no": row.get("invoice_no"), "error": str(exc)[:500]})
                print(f"[{index}/{len(rows)}] {row.get('invoice_no')} → FAILED")

    successful = len(results)
    unknown_results = [item for item in results if item["ground_truth"] == "UNKNOWN"]
    summary = {
        "endpoint": BASE_URL,
        "model": MODEL,
        "total_cases": len(rows),
        "successful": successful,
        "failed": len(failures),
        "success_rate": round(successful / len(rows), 4) if rows else 0,
        "accuracy": round(sum(item["correct"] for item in results) / successful, 4) if successful else 0,
        "unknown_accuracy": round(sum(item["correct"] for item in unknown_results) / len(unknown_results), 4) if unknown_results else 0,
        "average_elapsed_ms": round(sum(item["elapsed_ms"] for item in results) / successful, 2) if successful else 0,
        "total_elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
        "total_input_tokens": sum(item["input_tokens"] or 0 for item in results),
        "total_output_tokens": sum(item["output_tokens"] or 0 for item in results),
        "results": results,
        "failures": failures,
    }
    RESULT_FILE.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"成功：{successful}，失敗：{len(failures)}，準確率：{summary['accuracy']:.2%}")
    print(f"未知字軌準確率：{summary['unknown_accuracy']:.2%}")
    print(f"結果：{RESULT_FILE}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
