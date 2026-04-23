# 路由設計文件 (ROUTES) - 個人記帳簿系統

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁儀表板** | GET | `/` | `templates/index.html` | 顯示當月收支總計、圓餅圖分析與最新明細 |
| **收支明細列表** | GET | `/transactions` | `templates/transactions.html` | 顯示所有明細之表格，以及新增/編輯表單 |
| **建立收支明細** | POST | `/transactions` | — | 接收新增表單資料，寫入資料庫後重導回列表 |
| **更新收支明細** | POST | `/transactions/<id>/edit` | — | 接收編輯表單資料，更新特定紀錄並重導 |
| **刪除收支明細** | POST | `/transactions/<id>/delete` | — | 刪除單筆紀錄，完成後重導回列表 |
| **系統設定頁面** | GET | `/settings` | `templates/settings.html` | 顯示目前預算額度設定、與目前有的類別列表 |
| **更新當月預算** | POST | `/settings/budget` | — | 寫入或更新當月預算上限，並重導回設定頁面 |
| **新增自訂類別** | POST | `/settings/categories` | — | 接受新自訂類別，存入 DB 後歸位 |
| **刪除自訂類別** | POST | `/settings/categories/<id>/delete`| — | 防止預設被刪除的邏輯判斷，並移除使用者自訂類別 |

## 2. 每個路由的詳細說明

### 2.1 首頁儀表板 (Dashboard `app/routes/dashboard.py`)
- **GET `/`**
  - **輸入**：無（預設視為查詢當月）。
  - **處理邏輯**：利用 Transaction Model 查詢當月所有數據，加總各筆金額，並統計各類別的金額來產生分析圖表（如圓餅圖資料）；取得已設定的預算以供比較。
  - **輸出**：傳入參數給 `index.html` 進行渲染。
  - **錯誤處理**：若該月沒有資料，前端預設顯示「尚無紀錄」以及數字 0。

### 2.2 收支明細 (Transactions `app/routes/transaction.py`)
- **GET `/transactions`**
  - **處理邏輯**：呼叫 `Transaction.get_all()` 以及 `Category.get_all()` 得到完整明細及選項。
  - **輸出**：渲染 `transactions.html`。
- **POST `/transactions`**
  - **輸入**：來自前端表單的欄位 `amount`, `category_id`, `type`, `date`, `note`。
  - **處理邏輯**：建立 `Transaction`。如果本次新增後，當月總支出大於當月 `Budget` 設定上限，則產生系統的 Flash 警示通知。
  - **輸出**：執行後 `redirect(url_for('transaction.list_transactions'))`。
- **POST `/transactions/<id>/edit` 與 `/delete`**
  - **處理邏輯**：呼叫對應 id 進行修改、移除，處理方式均為送出處理後利用 `redirect` 重新讀取畫面，以避免重複送出表單。

### 2.3 系統設定與類別 (Settings `app/routes/settings.py`)
- **GET `/settings`**
  - **輸入**：無。
  - **處理邏輯**：取得出所有 Categories，取得單個當月 Budget 額度。
  - **輸出**：渲染 `settings.html`。
- **POST `/settings/budget`**
  - **輸入**：表單發送指定的 `amount` 上限。隱藏欄位或後端生成 `month` (YYYY-MM)。
  - **處理邏輯**：將結果更新至 `budgets` 資料表。
  - **輸出**：重導向至 `settings.view_settings`。
- **POST `/settings/categories` 與 `/delete`**
  - **處題邏輯**：新增與強制刪除。Model 在刪除時有針對 `is_default` 等於 `0` 的防呆防禦，如果前端嘗試刪除預設也會被 DB 擋下。

## 3. Jinja2 模板清單

1. `templates/base.html`：基底視圖。包含頂端 Header Navigation（導航到首頁/明細/設定）、Flash Message 顯示區塊，以及引入所需的 CSS 與 JS （如 Bootstrap, Chart.js）。
2. `templates/index.html`：繼承 `base.html`。呈現收支卡片、可用資金卡片，以及透過 JavaScript Canvas 繪製的開銷分佈圖。
3. `templates/transactions.html`：繼承 `base.html`。呈現以條列或格線方式顯示明細清單的外觀，畫面上方將留有一區塊作為「新增」。
4. `templates/settings.html`：繼承 `base.html`。雙欄排版或分區：左半處理「預算額度」輸入，右半處理「類別項目」的新增與刪除清單。

## 4. 路由骨架程式碼
開發階段採用 Blueprint 機制將路由拆分。`app/routes/` 檔案架構為：
- `__init__.py` : 提供 Blueprint 註冊入口
- `dashboard.py` : 首頁視圖與統計
- `transaction.py` : 資料收錄
- `settings.py` : 系統設定操作
