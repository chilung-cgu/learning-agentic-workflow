# Learning Agentic Workflow: GitHub Copilot CLI Edition

> [!NOTE]
> 此專案為練習 Agentic Workflow 的學習用途。我們把 GitHub 官方最新的 `@github/copilot` AI Agent 命令列工具放上了雲端，讓它每天自動幫我們追蹤並翻譯開源專案。

## 專案目的
這個專案實作了完全基於 **GitHub Copilot CLI** 的無頭 (Headless) 代理工作流：
1. **追蹤上游**：每日定時抓取最新版的 `github/copilot-cli` 開源專案。
2. **AI 代寫**：在雲端利用 `copilot --experimental --allow-all` 強制授權 Agent 自動比對英文文件，並進行繁體中文翻譯與覆寫。
3. **自動推播**：翻譯完成後，透過 GitHub Actions 自動 Commit 並 Push 回我們自己的 Repo。

## 事前準備與雲端授權 (極度重要！)
在本地端 `copilot cli` 可以彈出瀏覽器讓您登入，但在雲端的虛擬機中，您必須提供一把能夠存取 Copilot 權限的金鑰 (Token)：

1. 到 GitHub [Personal Access Tokens (Fine-grained)](https://github.com/settings/personal-access-tokens/new) 網頁。
2. 開啟 **Copilot Requests** 的權限，並產生一組 Token (`github_pat_xxxx`)。
3. 回到本練習 Repo 的 `Settings > Secrets and variables > Actions`。
4. 新增一組 Secret，命名為 **`COPILOT_PAT_SECRET`**，把剛才的 Token 貼進去。

大功告成！現在您可以到 GitHub 網站上切換到 **Actions** 頁籤，手動點擊 Run workflow 來觸發雲端翻譯了！
