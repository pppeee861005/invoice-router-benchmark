# 調用原生 Jev 的筆記

## 一、Jev 是什麼

Jev 是 TypeSafe AI 的結構化決策模型。它接收一段 `state` 與一組 typed questions，回傳程式可以直接使用的答案、機率與信心度。

Jev 適合用於：

- 客服問題分類
- 風險判斷
- 是否需要人工審查
- 工作流程分流
- 緊急程度判斷

Jev 不是一般文字生成模型，不應期待它產生長篇回答。

## 二、原生 API 資訊

原生 TypeSafe API：

```text
POST https://api.typesafe.ai/v1/systemone
```

模型名稱：

```text
jev-latest
```

認證方式：

```http
Authorization: Bearer <TypeSafe API Key>
Content-Type: application/json
```

官方文件建議使用 `TYPESAFE_API_KEY` 環境變數。

## 三、設定 `.env`

本專案測試檔使用：

```text
D:\code秋季115\practice_jev\jev_benchmark\.env
```

內容格式：

```env
TYPESAFE_API_KEY=你的_TypeSafe_API_Key
```

注意事項：

- 不要在 Key 前後加入空格。
- 不要把 Key 貼到 Git 或公開文件。
- 不要在終端機輸出完整 Key。
- TypeSafe 原生 Key 與 Vercel AI Gateway Key 不要混用。

## 四、問題類型

### 1. Choice

從指定選項中選出一個答案，回傳 `choice`、`confidence` 與 `probabilities`。

```json
{
  "type": "choice",
  "instructions": "這個問題應由哪個團隊處理？",
  "criteria": {
    "billing": "付款或訂閱問題",
    "technical": "錯誤或系統整合問題",
    "sales": "價格或帳戶問題"
  }
}
```

### 2. Score

依照指定的評分標準對 state 評分，回傳 `score`、`confidence` 與機率分布。

```json
{
  "type": "score",
  "instructions": "客戶看起來有多挫折？",
  "criteria": [
    "冷靜，只是在陳述事實",
    "感到挫折但仍有禮貌",
    "非常憤怒，使用強烈措辭"
  ]
}
```

### 3. Noul

判斷某個敘述是否成立，回傳 `noul`，數值範圍為 `0–1`。

```json
{
  "type": "noul",
  "instructions": "這則訊息是否表達急迫性？"
}
```

## 五、完整 Python 範例

```python
import os
import requests
from dotenv import load_dotenv


load_dotenv("jev_benchmark/.env")

api_key = os.getenv("TYPESAFE_API_KEY")
if not api_key:
    raise RuntimeError("找不到 TYPESAFE_API_KEY")

payload = {
    "model": "jev-latest",
    "state": "客戶無法連接 Stripe，已經影響銷售。",
    "questions": {
        "category": {
            "type": "choice",
            "instructions": "這個問題應由哪個團隊處理？",
            "criteria": {
                "billing": "付款或訂閱問題",
                "technical": "錯誤或系統整合問題",
                "sales": "價格或帳戶問題",
            },
        },
        "urgent": {
            "type": "noul",
            "instructions": "這則訊息是否表達急迫性？",
        },
    },
}

response = requests.post(
    "https://api.typesafe.ai/v1/systemone",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    },
    json=payload,
    timeout=30,
)
response.raise_for_status()
result = response.json()

print(result["answers"]["category"]["choice"])
print(result["answers"]["category"]["confidence"])
print(result["answers"]["urgent"]["noul"])
```

## 六、執行本專案測試

```powershell
cd D:\code秋季115\practice_jev
python test_native_jev.py
```

目前測試腳本：

```text
D:\code秋季115\practice_jev\test_native_jev.py
```

它會讀取 `jev_benchmark/.env`，送出一筆原生 Jev 請求，並顯示 HTTP 狀態、答案與 Token 使用量。

## 七、成功回應範例

```json
{
  "model": "jev-1.13.0",
  "answers": {
    "category": {
      "type": "choice",
      "choice": "technical",
      "confidence": 0.91
    },
    "urgent": {
      "type": "noul",
      "noul": 0.91
    }
  },
  "usage": {
    "input_tokens": 391,
    "output_tokens": 55
  }
}
```

## 八、常見錯誤

### HTTP 401

代表 API Key 無法通過 TypeSafe 原生 API 驗證。請確認 Key 來自 TypeSafe Dashboard，且 `.env` 欄位名稱是 `TYPESAFE_API_KEY`。

### HTTP 403

若是呼叫 Vercel AI Gateway，可能代表 Team 的 Free tier 沒有 Jev 存取權。這和原生 TypeSafe API 的認證是兩回事。

### HTTP 429

代表請求過於頻繁。應降低並行數量，加入指數退避與重試。

## 九、原生 API 與 Vercel Gateway 的差異

| 項目 | TypeSafe 原生 API | Vercel AI Gateway |
|---|---|---|
| Endpoint | `api.typesafe.ai/v1/systemone` | `ai-gateway.vercel.sh/v1/evaluate` |
| API Key | TypeSafe API Key | Vercel AI Gateway API Key |
| Model | `jev-latest` | `typesafe-ai/jev` |
| 問題類型 | `choice`、`score`、`noul` | Gateway 格式的 typed questions |
| 本專案腳本 | `test_native_jev.py` | `jev_benchmark/benchmark_jev.py` |

## 十、官方文件

- [TypeSafe Introduction](https://docs.typesafe.ai/introduction)
- [TypeSafe Quick Start](https://docs.typesafe.ai/introduction/quickstart)
