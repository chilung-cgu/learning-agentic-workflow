# GitHub Copilot CLI

GitHub Copilot 的強大功能，現在就在您的終端機中。

GitHub Copilot CLI 將 AI 驅動的程式設計協助功能直接帶入您的命令列，讓您能夠透過自然語言對話來建置、除錯與理解程式碼。採用與 GitHub 的 Copilot 程式設計代理相同的代理框架，在與您的 GitHub 工作流程深度整合的同時提供智慧協助。

請參閱[我們的官方文件](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)以取得更多資訊。

![Image of the splash screen for the Copilot CLI](https://github.com/user-attachments/assets/f40aa23d-09dd-499e-9457-1d57d3368887)


## 🚀 介紹與概覽

我們正在將 GitHub Copilot 程式設計代理的強大功能直接帶入您的終端機中。透過 GitHub Copilot CLI，您可以在本機與一個了解您的程式碼及 GitHub 上下文的 AI 代理同步協作。

- **終端機原生開發：** 直接在您的命令列中與 Copilot 程式設計代理協作 — 無需切換上下文。
- **開箱即用的 GitHub 整合：** 使用自然語言存取您的儲存庫、議題與拉取請求，全部都透過您現有的 GitHub 帳號進行身份驗證。
- **代理能力：** 與可以規劃並執行複雜任務的 AI 協作者一起建置、編輯、除錯與重構程式碼。
- **MCP 驅動的擴充性：** 利用程式設計代理預設搭載 GitHub 的 MCP 伺服器的優勢，並支援自訂 MCP 伺服器來擴充功能。
- **完全控制：** 在執行前預覽每個動作 — 沒有您的明確批准，什麼都不會發生。

我們仍處於旅程的早期階段，但透過您的回饋，我們正在快速迭代，以使 GitHub Copilot CLI 成為您終端機中最佳的夥伴。

## 📦 開始使用

### 支援的平台

- **Linux**
- **macOS**
- **Windows**

### 先決條件

- （在 Windows 上）**PowerShell** v6 或更高版本
- 一個**有效的 Copilot 訂閱**。請參閱 [Copilot 方案](https://github.com/features/copilot/plans?ref_cta=Copilot+plans+signup&ref_loc=install-copilot-cli&ref_page=docs)。

如果您是透過組織或企業存取 GitHub Copilot，若您的組織擁有者或企業管理員已在組織或企業設定中停用它，您將無法使用 GitHub Copilot CLI。請參閱[管理組織中 GitHub Copilot 的政策和功能](http://docs.github.com/copilot/managing-copilot/managing-github-copilot-in-your-organization/managing-github-copilot-features-in-your-organization/managing-policies-for-copilot-in-your-organization)以取得更多資訊。

### 安裝

使用安裝腳本安裝（macOS 和 Linux）：

```bash
curl -fsSL https://gh.io/copilot-install | bash
```

或

```bash
wget -qO- https://gh.io/copilot-install | bash
```

使用 `| sudo bash` 以 root 身份執行並安裝到 `/usr/local/bin`。

設定 `PREFIX` 以安裝到 `$PREFIX/bin/` 目錄。預設為 `/usr/local`
（以 root 身份執行時）或 `$HOME/.local`（以非 root 使用者身份執行時）。

設定 `VERSION` 以安裝特定版本。預設為最新版本。

例如，要將版本 `v0.0.369` 安裝到自訂目錄：

```bash
curl -fsSL https://gh.io/copilot-install | VERSION="v0.0.369" PREFIX="$HOME/custom" bash
```

使用 [Homebrew](https://formulae.brew.sh/cask/copilot-cli) 安裝（macOS 和 Linux）：

```bash
brew install copilot-cli
```

```bash
brew install copilot-cli@prerelease
```


使用 [WinGet](https://github.com/microsoft/winget-cli) 安裝（Windows）：

```bash
winget install GitHub.Copilot
```

```bash
winget install GitHub.Copilot.Prerelease
```


使用 [npm](https://www.npmjs.com/package/@github/copilot) 安裝（macOS、Linux 和 Windows）：

```bash
npm install -g @github/copilot
```

```bash
npm install -g @github/copilot@prerelease
```


### 啟動 CLI

```bash
copilot
```

首次啟動時，您將看到我們可愛的動畫橫幅！如果您想再次看到此橫幅，請使用 `--banner` 旗標啟動 `copilot`。

如果您目前尚未登入 GitHub，系統將提示您使用 `/login` 斜線命令。輸入此命令並遵循螢幕上的指示進行身份驗證。

#### 使用個人存取權杖（PAT）進行身份驗證

您也可以使用啟用了「Copilot Requests」權限的細粒度 PAT 進行身份驗證。

1. 造訪 https://github.com/settings/personal-access-tokens/new
2. 在「Permissions」下，點擊「add permissions」並選擇「Copilot Requests」
3. 產生您的權杖
4. 透過環境變數 `GH_TOKEN` 或 `GITHUB_TOKEN`（依優先順序）將權杖新增到您的環境中

### 使用 CLI

在包含您想要處理的程式碼的資料夾中啟動 `copilot`。

預設情況下，`copilot` 使用 Claude Sonnet 4.5。執行 `/model` 斜線命令以從其他可用的模型中選擇，包括 Claude Sonnet 4 和 GPT-5。

### 實驗模式

實驗模式可讓您存取仍在開發中的新功能。您可以透過以下方式啟用實驗模式：

- 使用 `--experimental` 旗標啟動：`copilot --experimental`
- 在 CLI 內使用 `/experimental` 斜線命令

一旦啟用，此設定將保存在您的配置中，因此在後續啟動時不再需要 `--experimental` 旗標。

#### 實驗功能

- **自動駕駛模式：** 自動駕駛是一種新模式（按 `Shift+Tab` 在模式之間切換），它鼓勵代理持續工作直到任務完成。

每次您向 GitHub Copilot CLI 提交提示時，您的每月高級請求配額將減少一個。有關高級請求的資訊，請參閱[關於高級請求](https://docs.github.com/copilot/managing-copilot/monitoring-usage-and-entitlements/about-premium-requests)。

有關如何使用 GitHub Copilot CLI 的更多資訊，請參閱[我們的官方文件](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)。

## 🔧 配置 LSP 伺服器

GitHub Copilot CLI 支援語言伺服器協定（LSP）以增強程式碼智慧。此功能提供智慧程式碼功能，如跳轉至定義、懸停資訊和診斷。

### 安裝語言伺服器

Copilot CLI 不內建 LSP 伺服器。您需要單獨安裝它們。例如，要設定 TypeScript 支援：

```bash
npm install -g typescript-language-server
```

對於其他語言，請安裝相應的 LSP 伺服器並按照以下所示的相同模式進行配置。

### 配置 LSP 伺服器

LSP 伺服器透過專用的 LSP 配置檔案進行配置。您可以在使用者層級或儲存庫層級配置 LSP 伺服器：

**使用者層級配置**（適用於所有專案）：
編輯 `~/.copilot/lsp-config.json`

**儲存庫層級配置**（適用於特定專案）：
在您的儲存庫根目錄中建立 `.github/lsp.json`

範例配置：

```json
{
  "lspServers": {
    "typescript": {
      "command": "typescript-language-server",
      "args": ["--stdio"],
      "fileExtensions": {
        ".ts": "typescript",
        ".tsx": "typescript"
      }
    }
  }
}
```

### 檢視 LSP 伺服器狀態

使用互動式工作階段中的 `/lsp` 命令檢查已配置的 LSP 伺服器，或直接檢視您的配置檔案。

有關更多資訊，請參閱[變更日誌](./changelog.md)。

## 📢 回饋與參與

我們很高興您能在 Copilot CLI 旅程的早期加入我們。

我們正在快速建置。預期會有頻繁的更新 — 請保持您的客戶端更新，以獲得最新的功能和修復！

您的見解非常寶貴！在此儲存庫中開啟議題、加入討論，並從 CLI 執行 `/feedback` 以提交機密回饋調查！
