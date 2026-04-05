# Learning Agentic Workflow (練習專案)

> [!NOTE]
> 此專案為練習自動化 Agentic Workflow 的用途，絕非抄襲，僅用於學習 GitHub Actions 與 AI Agent 之應用。

## 專案目的
這個專案演示了如何實作一個「全自動化」的代理工作流：
1. **觸發**：每天定時在 GitHub 雲端執行。
2. **準備**：將開源界著名的 `octocat/Hello-World` 專案 (Upstream) 的 README.md 拉取下來。
3. **代理**：在雲端執行 `translate-agent.py`，並安全地將 `GEMINI_API_KEY` 作為環境變數傳入，呼叫 Google Gemini，翻譯為繁體中文。
4. **提交**：比對差異後，如果翻譯有更新，則由 `github-actions[bot]` 自動發布 Commit。

## 如何開始 (本地測試)
如果你要在本地測試（不依靠 Github Action），你可以：
1. 建立對應的目錄 `repos/upstream/` 放原版檔案，`repos/current/` 放目前檔案。
2. 設定環境變數 `export GEMINI_API_KEY=你的金鑰`
3. 執行 `python translate-agent.py`
