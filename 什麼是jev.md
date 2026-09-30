# 什麼是 Jev？

## 簡介

Jev 是 **TypeSafe AI** 開發的 AI 模型，也是 TypeSafe 第一個 **System One Model**。

Jev 的設計目標不是聊天或產生長篇文章，而是讓軟體快速取得可直接使用的結構化判斷。

簡單理解：

> 一般 LLM 產生文字；Jev 產生程式可以直接使用的決策。

## Jev 可以做什麼？

Jev 適合以下工作：

- 客戶訊息分類
- 對話路由與分派
- 判斷訊息是否緊急
- 評估客戶情緒或風險
- 判斷是否需要人工審核
- 驗證其他 AI 模型的輸出
- 選擇下一個工具、模型或工作流程分支

例如，可以請 Jev 判斷一段客戶訊息是「付款問題」、「技術問題」還是「客訴」，再由程式把訊息分派給正確部門。

## Jev 的輸出類型

官方文件目前主要介紹三種問題類型：

| 類型 | 用途 | 輸出 |
|---|---|---|
| Choice | 從多個選項中選擇 | 選項、機率、信心度 |
| Score | 依評分標準評估 | 分數、機率、信心度 |
| Boolean／Noul | 判斷真假 | 真假機率 |

Jev 的問題與選項需要預先定義，因此它適合「有限選項的決策」，不適合要求它自由創作文字。

## Jev 與 ChatGPT、Gemini 的差異

| 項目 | 一般 LLM | Jev |
|---|---|---|
| 主要輸出 | 文字 | 結構化決策 |
| 適合用途 | 對話、摘要、寫作、程式生成 | 分類、評分、路由、驗證 |
| 輸出方式 | 逐 token 產生 | 對預先定義的問題做判斷 |
| 是否適合直接寫淨化後文章 | 適合 | 不適合單獨使用 |
| 是否提供信心資訊 | 不一定可靠 | 會回傳機率或信心資訊 |

在「客戶對話淨化」專案中，Jev 可以先判斷對話類別、敏感程度或是否需要人工審核；真正改寫文字，仍應交給 Gemini、GPT 或其他文字生成模型。

## 官方資料中的特色

TypeSafe 將 Jev 定位為快速、可組合、具型別安全的決策模型，並使用 **RLCD（Reinforcement Learning for Calibrated Decisions）** 作為訓練方法。

官方宣稱 Jev 的輸入價格為每十億 input tokens 約 42 美元，並在特定工作流程中具有很低延遲；這些數據應視為官方測試結果，不代表所有任務都會得到相同效能。

## 名稱來源

官方說明 Jev 的名稱來自經濟學家 **William Stanley Jevons**。

## 注意事項

- Jev 目前以 early access 形式提供，實際 API 權限可能受帳戶狀態影響。
- Jev 不是一般聊天模型，不能只傳一個「請介紹你自己」的聊天訊息來測試。
- API 金鑰不可寫入公開 Git 儲存庫或貼到聊天內容中。
- 官方聲稱的速度、價格與準確度需要在自己的工作流程中實測。

## 官方連結

- [TypeSafe AI 官方公告](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
- [TypeSafe 官方文件](https://docs.typesafe.ai/introduction)
- [Vercel Jev 模型頁面](https://vercel.com/ai-gateway/models/jev)
