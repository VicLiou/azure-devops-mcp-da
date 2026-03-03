# azure-devops-mcp-da

本專案旨在提供一個客製化的 Azure DevOps MCP Server，用於管理 Azure DevOps 的工作項目。這是一個基於 Python 及 `mcp.server.fastmcp` 實作的 Server，專門為了安全且受控地管理與操作 Azure DevOps 工作項目所設計。本專案能有效地橋接 AI 助理與企業內部的 Azure DevOps 系統，並內建權限防護與資料加密機制。

## 客製化功能與特色

- **嚴謹的權限控管**：新增/刪除項目的功能遭限縮，使用者與 AI 僅能新增刪除自己的項目，防範意外覆寫或刪除他人資料。
- **自動化映射管理 (Mapping Table)**：透過 `resources/mapping_table.json` 維護組織、部門與專案的代碼或名稱映射，AI 在建立工作或處理資料時，即可自動套用正確的欄位資訊而無須額外設定。
- **任務樣板支援 (Task Templates)**：藉由 `resources/task_templates.py` 檔案定義各式工作項目模板。MCP 會將這些模板註冊為 Resource，利於 AI 快速建立標準化格式的工作項目。
- **高等級資料加密保護 (GCM)**：敏感路徑與設定檔皆透過 `cryptography` 套件進行 AES-GCM 加密驗證，減少組態檔被意外修改的風險。

## 專案架構與模組解析

- **`server.py`**：整個 MCP Server 的主入口點，負責環境變數讀取、連線驗證及啟動註冊 MCP 的各項核心功能（Tools、Resources、Prompts）。
- **`init.py`**：主控 Azure DevOps 的 API 連線與全域設定初始化 (`McpConfig`, `initialize_global_connector`)。
- **`/tool/` 目錄**：向 AI 暴露的操作指令（MCP Tools），包含：
  - `search_tool.py`: 查詢與篩選 Azure DevOps 上的工作項目。
  - `create_item_tool.py`: 透過樣板與映射表安全地建立工作項目。
  - `delete_item_tool.py`: 刪除指定工作項目（內建身分驗證，限縮於自有項目）。
  - `add_mapping_table_tool.py`: 動態為系統新增 Mapping Table 條目。
- **`/resources/` 目錄**：放置主要設定材料，包含 `mapping_table.json` 及 `task_templates.py`。
- **`/prompt/` 目錄**：包含提供給 AI 端使用的對話上下文範本（`prompt_template.py`）。
- **`/sources/` 目錄**：實作將本專案資源註冊至 MCP 的介面，如 `template_source.py` 會將樣板轉為 MCP Resource 結構。
- **`/config/` 與 `/utils/` 目錄**：負責基礎設施服務，包含 `logging_config.py` 日誌處理系統與 `init_util.py` 環境變數處理。

## 針對 AI 開發與擴充的建議方向

如果您（AI）將要擴充或修正此專案，請參考以下準則：

1. **新增工具（Tools）時**：請放置於 `/tool` 資料夾底下，在 `server.py` 完成導入並寫明詳細的 `@mcp.tool()` 註解說明，清晰的 tool 描述可大幅提升 AI 的辨識率與可用度。
2. **新增流程範本時**：如果想要提供新的提示（Prompt）給大語言模型使用，請將邏輯加入 `/prompt/prompt_template.py`。
3. **保持安全性檢查**：若加入修改項目的 Tool 時，務必在內部引用或實作身分檢查邏輯，避免跨域或跨使用者修改的風險。

## 使用 azure-devops-mcp-da MCP Server

### Python 版本要求

- Python 3.13.2 or upper

### 需安裝套件

- **mcp :** MCP Server 套件
- **cryptography :** GCM 加解密套件

### 建立 Python 虛擬環境

範例使用 Miniconda 建立 Python 虛擬環境

``` powershell
# 建立虛擬環境
conda create -n azure-devops-mcp python=3.13.2

# 啟動虛擬環境
conda activate azure-devops-mcp

# 安裝套件
pip install mcp
pip install cryptography
```

### 設定 MCP Server 環境變數

#### 一、環境變數說明

此 Server 必須取得以下環境變數方能順利啟動：

| 變數名稱         | 說明                                                     |
| ---------------- | -------------------------------------------------------- |
| `TFS_URL`        | Azure DevOps 伺服器之根網址連線位址                      |
| `TFS_CERT`       | TLS/SSL 自架憑證的絕對路徑（若無則免）                   |
| `USER_TOKEN`     | Azure DevOps 產生的個人存取權杖（Personal Access Token） |
| `DECRYPTION_KEY` | 來自組態加密程式所配發之設定檔解密金鑰                   |
| `ENC_FILE_DICT`  | 加密處理後的字典設定檔路徑/資料                          |
| `ENC_FILE_JSON`  | 加密處理後的 JSON 設定檔路徑/資料                        |

#### 二、環境變數設定範例

- 使用 Python 執行檔

``` json
{
    "servers": {
        "da-azure-devops": {
            "type": "stdio",
            // 指向虛擬環境的 python 執行檔
            "command": "D:\\Users\\user1\\azure-devops-mcp\\Scripts\\python.exe",
            "args": [
                // 指向專案內的 server.py
                "D:\\workspace\\mcp\\azure-devops-mcp-da\\server.py"
            ],
            "env": {
                "TFS_URL": "https://azure-devops/tfs/DefaultCollection",
                "TFS_CERT":"C:\\temp\\azure-devops.crt",
                "USER_TOKEN": "rvzkv4kpkny6wiavpe56fulh5g4g3vgzttmscolmelbnmcgs222q",
                "DECRYPTION_KEY": "cc8884164f8bf80c060f57a47c13ca8a",
                "ENC_FILE_DICT": "hLVfdUHbOOhayus2-D2J8_3DWM5po22MsQbwQa7EOtVXa8BjOIKUOH_oAqu8fPSM4MECotQDcrysUFtx_ImBGBiY82eUQmBzFhVjuoIB3Dg3dPAevEx922N_VnO0R2m02oRrc_lFipnRImmXOWKf3RMBAj-9bQ7HpH8886eA1ZWvqNxUHiDKX2LCXhpd",
                "ENC_FILE_JSON": "0m4MzdWmg_yr9BTIN2Hq7VQ777WYkv7X_Qmc6W371aOJqRyXJRU4cDAOHh0is3H4tLoQhCwfHDYbC-YJmY6ynHR5sm03ZezKoaSN0RDlRt8j3KdNzIy-c0eJ8C724viXd9c28JiZ1jf-O-c-Xdnet08pIpr0VxgqoepLvZRwwMZYJIQhZWWgFq_Pueim7A=="
            }
        }
    }
}
```

- 使用 exe 執行檔

``` json
{
    "servers": {
        "da-azure-devops": {
            "type": "stdio",
            "command": "D:\\workspace\\mcp\\azure-devops-mcp-da.exe",
            "env": {
                "TFS_URL": "https://azure-devops/tfs/DefaultCollection",
                "TFS_CERT":"C:\\temp\\azure-devops.crt",
                "USER_TOKEN": "rvzkv4kpkny6wiavpe56fulh5g4g3vgzttmscolmelbnmcgs222q",
                "DECRYPTION_KEY": "cc8884164f8bf80c060f57a47c13ca8a",
                "ENC_FILE_DICT": "hLVfdUHbOOhayus2-D2J8_3DWM5po22MsQbwQa7EOtVXa8BjOIKUOH_oAqu8fPSM4MECotQDcrysUFtx_ImBGBiY82eUQmBzFhVjuoIB3Dg3dPAevEx922N_VnO0R2m02oRrc_lFipnRImmXOWKf3RMBAj-9bQ7HpH8886eA1ZWvqNxUHiDKX2LCXhpd",
                "ENC_FILE_JSON": "0m4MzdWmg_yr9BTIN2Hq7VQ777WYkv7X_Qmc6W371aOJqRyXJRU4cDAOHh0is3H4tLoQhCwfHDYbC-YJmY6ynHR5sm03ZezKoaSN0RDlRt8j3KdNzIy-c0eJ8C724viXd9c28JiZ1jf-O-c-Xdnet08pIpr0VxgqoepLvZRwwMZYJIQhZWWgFq_Pueim7A=="
            }
        }
    }
}
```

### 啟動 MCP Inspector

- 直接使用 Python 專案

``` powershell
npx -y @modelcontextprotocol/inspector `
-e "TFS_URL=https://azure-devops/tfs/DefaultCollection" `
-e "TFS_CERT=C:\\temp\\azure-devops.crt" `
-e "USER_TOKEN=rvzkv4kpkny6wiavpe56fulh5g4g3vgzttmscolmelbnmcgs222q" `
-e "DECRYPTION_KEY=cc8884164f8bf80c060f57a47c13ca8a" `
-e "ENC_FILE_DICT=hLVfdUHbOOhayus2-D2J8_3DWM5po22MsQbwQa7EOtVXa8BjOIKUOH_oAqu8fPSM4MECotQDcrysUFtx_ImBGBiY82eUQmBzFhVjuoIB3Dg3dPAevEx922N_VnO0R2m02oRrc_lFipnRImmXOWKf3RMBAj-9bQ7HpH8do6eA1ZWvqNxUHiDKX2LCXhpd" `
-e "ENC_FILE_JSON=0m4MzdWmg_yr9BTIN2Hq7VQ757WYkv7X_Qmc6W371aOJqRyXJRU4cDAOHh0is3H4tLoQhCwfHDYbC-YJmY6ynHR5sm03ZezKoaSN0RDlRt8j3KdNzIy-c0eJ8C724viXd9c28JiZ1jf-O-c-Xdnet08pIpr0VxgqoepLvZRwwMZYJIQhZWWgFq_Pueim7A==" `
  -- `
"D:\\Users\\user1\\azure-devops-mcp\\Scripts\\python.exe" `
"D:\\gitSpace\\mcp\\azure-devops-da\\server.py"
```

- 使用打包後的 exe 檔

``` powershell
npx -y @modelcontextprotocol/inspector `
-e "TFS_URL=https://azure-devops/tfs/DefaultCollection" `
-e "TFS_CERT=C:\\temp\\azure-devops.crt" `
-e "USER_TOKEN=rvzkv4kpkny6wiavpe56fulh5g4g3vgzttmscolmelbnmcgs222q" `
  -- `
"D:\\gitSpace\\mcp\\azure-devops-da\\dist\\server.exe"
```

## 將 azure-devops-mcp-da 打包成 .exe 執行檔

- 安裝 pyinstaller

``` shell
pip install pyinstaller
```

- 打包成 .exe 執行檔

``` shell
pyinstaller -F server.py
```

※ 啟動後若遇到 No module named 'azure.devops.v7_0.location' 問題

1. 打開 server.spec

2. 在 hiddenimports=[]，加上 'azure.devops.v7_0.location'
