# 流程圖設計 (FLOWCHART) - 個人記帳簿系統

## 1. 使用者流程圖 (User Flow)

這張流程圖展示了使用者在網站上操作的主要路徑，涵蓋操作儀表板、管理收支明細，以及進行自訂類別與預算設定。

```mermaid
flowchart LR
    Start([使用者開啟網站]) --> Dashboard[首頁 - 儀表板]
    
    Dashboard --> ActionChoice{要執行什麼操作？}
    
    ActionChoice -->|查看統計| ViewStats[檢視當月總收支、餘額與消費比例圓餅圖]
    ViewStats --> Dashboard
    
    ActionChoice -->|管理紀錄| ViewRecords[進入收支明細頁面]
    ViewRecords --> RecordAction{對明細的操作}
    RecordAction -->|新增| AddRecord[填寫並送出新增收支表單]
    RecordAction -->|編輯| EditRecord[修改現有的收支紀錄]
    RecordAction -->|刪除| DeleteRecord[確認並刪除指定的紀錄]
    AddRecord --> ViewRecords
    EditRecord --> ViewRecords
    DeleteRecord --> ViewRecords
    ViewRecords --> Dashboard
    
    ActionChoice -->|系統設定| Settings[進入系統設定頁面]
    Settings --> SettingAction{設定項目}
    SettingAction -->|類別管理| ManageCategories[新增或刪除自訂收支類別]
    SettingAction -->|預算設定| SetBudget[設定當月總預算]
    ManageCategories --> Settings
    SetBudget --> Settings
    Settings --> Dashboard
```

## 2. 系統序列圖 (Sequence Diagram)

這張序列圖描述了本系統的核心功能：「使用者新增一筆支出紀錄，同時系統檢查是否超過預算」的詳細資料流動過程與元件互動關係。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (前端)
    participant Flask as Flask Route (Controller)
    participant Model as Database Model
    participant DB as SQLite
    
    User->>Browser: 在表單填寫支出金額、類別與日期，點擊送出
    Browser->>Flask: POST /transactions (送出表單資料)
    activate Flask
    
    %% 新增紀錄流程
    Flask->>Model: 建立 Transaction 物件
    activate Model
    Model->>DB: INSERT INTO transactions (金額, 類別, 日期)
    DB-->>Model: 寫入成功
    Model-->>Flask: 回傳最新紀錄狀態
    deactivate Model
    
    %% 驗證是否超支流程
    Flask->>Model: 查詢當月「總支出」與「當月預算上限」
    activate Model
    Model->>DB: 執行 SELECT SUM(...) 與 SELECT budget...
    DB-->>Model: 回傳總支出與預算數字
    Model-->>Flask: 回傳運算所需數據
    deactivate Model
    
    alt 總支出 > 當月預算
        Flask-->>Flask: 設定警示訊息 (Flash Message:⚠️ 預算已超支！)
    else 總支出 <= 當月預算
        Flask-->>Flask: 設定成功訊息 (Flash Message:✅ 紀錄新增成功)
    end
    
    Flask-->>Browser: HTTP 302 重導向回 /transactions 列表頁
    deactivate Flask
    Browser->>User: 顯示最新明細，並且跳出 Flash 提示訊息
```

## 3. 功能清單對照表

本表列出系統每個功能所對應的 URL 路徑、HTTP 方法與負責的邏輯，這將作為開發階段 API 與路由設計的基礎。

| 功能區塊 | HTTP 方法 | URL 路徑 | 用途說明 |
| :--- | :--- | :--- | :--- |
| **儀表板** | GET | `/` | 系統首頁，顯示本月餘額總結、最新紀錄預覽與分類圓餅圖。 |
| **收支明細** | GET | `/transactions` | 以列表形式列出所有的收支明細紀錄。 |
| **收支明細** | POST | `/transactions` | 接收表單資料，新增一筆收支紀錄。 |
| **收支明細** | POST | `/transactions/<id>/edit` | 修改特定 ID 的收支紀錄。 |
| **收支明細** | POST | `/transactions/<id>/delete` | 刪除特定 ID 的收支紀錄。 |
| **設定/類別** | GET | `/settings` | 顯示預算設定與類別管理的介面。 |
| **設定/類別** | POST | `/settings/budget` | 接收表單資料，更新當月的預算設定。 |
| **設定/類別** | POST | `/settings/categories` | 接收表單資料，新增一筆自訂類別。 |
| **設定/類別** | POST | `/settings/categories/<id>/delete`| 刪除特定的自訂類別。 |

> **備註：**
> 由於標準的 HTML `<form>` 表單僅支援 `GET` 與 `POST` 方法，實作上我們用 `POST` 搭配 URL 結尾的 `/edit` 或 `/delete` 來處理修改與刪除的請求，而不是嚴格的 RESTful (PUT/DELETE) 設計，以減輕純後端渲染架構的負擔。
