# 發票期別路由器 Benchmark

本專案比較三種方法依發票號碼判斷期別的能力：Python 規則、LLM 與 TypeSafe 原生 Jev。目前已完成 Python Baseline 與 Jev 原生 API 測試。

## 專案設定

需要 Python 3.10 以上，並安裝套件：

```powershell
pip install requests python-dotenv
```

複製 `.env.example` 為 `.env`，再填入 TypeSafe API Key：

```env
TYPESAFE_API_KEY=你的_TypeSafe_API_Key
```

`.env` 只供本機使用，已加入 `.gitignore`，不可提交至 Git。

## 執行 Python 規則 Baseline

```powershell
cd D:\code秋季115\發票路由器專案計劃
python python_rule_baseline.py
```

程式讀取 `test.csv`，依前兩碼字軌判斷期別，並輸出 `python_rule_results.csv`。

## 執行原生 Jev 批次測試

```powershell
cd D:\code秋季115\發票路由器專案計劃
python jev_native_batch.py
```

程式使用 TypeSafe 原生 API：

```text
Endpoint: https://api.typesafe.ai/v1/systemone
Model: jev-latest
```

測試結果會輸出至 `jev_native_results.json`。結果檔案包含預測、正確性、信心度、延遲及 Token 使用量，已由 `.gitignore` 排除。

## 資料集

`test.csv` 共 100 筆：90 筆已知字軌、10 筆未知字軌。期別規則與資料格式請參考 `虛構「字軌 → 期別」簡易規則 v0.1.md`。

## 測試結果

目前結果請參考 [測試報告.md](測試報告.md)。
