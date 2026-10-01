# WTMH Lab Deck System — 設計系統規格文件

> WTMH 實驗室的共用簡報設計系統，最早從神經復健組的 VRMT 簡報（34 張）萃取。
> 用途：之後要做新的 deck 時，照這份文件複製 token、套版面骨架、沿用元件，就能得到一致的視覺。
> 設計系統來源檔：VRMT `slides.html` · 萃取日期：2026-05-19

---

## 1. 概述

| 項目 | 規格 |
|---|---|
| 畫布尺寸 | **1280 × 720 px**（16:9，固定像素，非 responsive） |
| 投影片圓角 | `border-radius:6px` |
| Deck 排列 | 直向 flex column，投影片間距 `gap:32px` |
| 頁面外距 | `body{ padding:40px 0 }`，deck `margin:0 auto` 置中 |
| Deck 背景 | `#3A3D45`（深灰，襯托白色投影片） |
| 投影片背景 | `#FFFFFF` + 微弱 radial-gradient |
| 投影片陰影 | `box-shadow:0 30px 60px -25px rgba(0,0,0,.55), 0 2px 6px rgba(0,0,0,.18)` |
| 設計語言 | 學術／醫療研究風格：serif 標題 + sans 內文，紅色品牌主軸，留白克制 |

整份 deck 是**單一 inline HTML 檔**：所有 CSS 在 `<head><style>` 內，所有圖片以 base64 data-URI 內嵌，字體用 Google Fonts CDN。沒有外部相依，單檔即可開。

---

## 2. 設計 Token

### 2.1 色彩（`:root` CSS variables）

```css
:root{
  --red:        #B7282E;   /* 品牌主色：標題左邊框、footer、強調 */
  --red-deep:   #8E1A20;   /* footer 漸層的深色端 */
  --ink:        #1B2030;   /* 主要文字（標題、重點字） */
  --ink-soft:   #3C4253;   /* 次要文字（內文、bullet） */
  --muted:      #6B7388;   /* 弱化文字（eyebrow、cite、label） */
  --line:       #E2E5EC;   /* 邊框、分隔線 */
  --teal:       #0E9FBA;   /* 第二強調色：縮寫、技術名詞、outcome */
  --amber:      #D96A18;   /* 第三強調色：卡片變體、章節漸層尾端 */
}
```

固定色（未進 token，但全檔通用）：
- 投影片底 `#FFFFFF` · Deck 底 `#3A3D45`
- 卡片淺底 `#FAFBFC` / `#FAF5F5`
- 半透明強調底：`rgba(183,40,46,.10)`（紅）、`rgba(14,159,186,.12)`（teal）、`rgba(217,106,24,.12)`（amber）

### 2.2 字體家族

| 角色 | font-family | 字重 | 用途 |
|---|---|---|---|
| Serif（標題） | `'Crimson Pro','Noto Serif TC',Georgia,serif` | 400 / 600 / 700 · italic 500 | 所有 h1/h2/h3、concept-lead、pageno |
| Sans（內文／UI） | `'Inter','Noto Sans TC',-apple-system,'Segoe UI',Roboto,sans-serif` | 300/400/500/600/700 | bullet、label、eyebrow、subtitle |
| Mono（程式碼） | `'Consolas','JetBrains Mono',monospace` | — | `.eng-badge` 技術規格條 |

Google Fonts 載入字串（放 `<head>`）：
```html
<link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,600;0,700;1,500&family=Inter:wght@300;400;500;600;700&family=Noto+Sans+TC:wght@400;500;700&family=Noto+Serif+TC:wght@500;700&display=swap" rel="stylesheet" />
```

---

## 3. 字體階層（Typography Scale）

| 層級 | size / weight / family | 行高 | 字距 | 出現處 |
|---|---|---|---|---|
| 封面主標 h1 | 50px · 700 · Crimson | 1.1 | -.5px | slide-title |
| 章節大標 | 88px · 700 · Crimson | 1.02 | -1.4px | chapter-break |
| 內容頁 h2 | 40px · 700 · Crimson | 1.1 | -.3px | content-chrome |
| 卡片 h3 | 26px · 700 · Crimson | 1.2 | — | `.card` |
| pipeline 步驟 h3 | 22px · 700 · Crimson | 1.15 | — | `.pipeline .step` |
| concept-lead 引言 | 21px · italic · Crimson | 1.45 | — | 內容頁開場句 |
| 內文 bullet | 17.5px · 400 · Inter | 1.55 | — | `.card ul li` |
| subtitle / eyebrow | 13–14px · 600 · Inter · UPPERCASE | — | .14–.22em | 副標、標籤 |
| cite-line 出處 | 12.5px · 400 · Inter | — | .02em | 投影片底參考文獻 |
| eng-badge 規格條 | 12.5px · Mono | 1.5 | — | 技術參數列 |
| micro-label | 10.5–11px · 700 · UPPERCASE | — | .18–.32em | step-no、pl-label |

**慣例**：所有 serif 標題用 Crimson Pro；所有小寫標籤一律 `text-transform:uppercase` + 寬字距（letter-spacing ≥ .16em）。

---

## 4. 投影片骨架（3 種 Slide Chrome）

每張 `<section>` 是一個獨立投影片。三種骨架類型：

### 4.1 封面 — `slide slide-title`

```
┌────────────────────────────────────────┐
│  top-deco（橫幅裝飾，z-index:5）          │
│                                          │
│  hero（grid 360px | 1fr）                │
│   ├ hero-art（圓環 + 主視覺圖）            │
│   └ hero-text（eyebrow / h1 / subtitle / │
│                pitch-line / affiliation）│
│                                          │
│  title-foot（夥伴 logo）  presenter-card  │
└────────────────────────────────────────┘
```
- `hero`：`position:absolute; top:145px; left:60px; right:60px; bottom:160px; display:grid; grid-template-columns:360px 1fr; gap:42px`
- `pitch-line`：紅色左邊框 `border-left:3px solid var(--red)` 的一句話定位語
- `presenter-card`：右下白卡，`border-left:6px solid var(--red)`，講者姓名 + meta

### 4.2 內容頁 — `slide content-chrome`（主力版型，全 deck ~28 張）

```
┌────────────────────────────────────────┐
│ ▟ 紅色 tab（::before, 170×14px 左上角）   │
│                                          │
│  page-head ── h2（6px 紅左框）+ subtitle │
│  ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄ │
│  content-body                            │
│   (top:138 left:60 right:60 bottom:108)  │
│   └ concept-lead → 主內容 → cite-line     │
│  ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄ │
│  footer-ribbon（logo + 紅色斜切條 + 頁碼）│
└────────────────────────────────────────┘
```

關鍵定位值（**新版型一定要遵守**）：

| 區塊 | CSS |
|---|---|
| 左上紅 tab | `::before` `top:0;left:0;width:170px;height:14px;background:var(--red);z-index:6` |
| page-head | `position:absolute;top:34px;left:60px;right:60px;z-index:7` |
| h2 標題 | Crimson 40px/700 · `padding-left:20px;border-left:6px solid var(--red)` |
| content-body | `position:absolute;top:138px;left:60px;right:60px;bottom:108px;display:flex;flex-direction:column;overflow:hidden` |
| footer-ribbon | `position:absolute;left:0;right:0;bottom:0;height:60px;z-index:8` |
| vr-bg 浮水印 | 右側 SVG，`opacity:.05`，`z-index:1` |

→ 可用內容高度 = 720 − 138 − 108 = **474px**。所有卡片／圖表必須塞進這個範圍，否則 `overflow:hidden` 會裁掉。

footer-ribbon 三件式：白底 logo 區 `.fl-left` ＋ 紅色漸層斜切條 `.ribbon-bar`（`clip-path:polygon(36px 0,100% 0,100% 100%,0 100%)`）＋ 圓形頁碼 `.pageno`（38×38 白底紅字）。

### 4.3 章節分頁 — `slide chapter-break`

```
┌────────────────────────────────────────┐
│ │ ch-rule（紅→琥珀漸層豎條）              │
│ │                              0 1      │
│ │  CHAPTER 0N（eyebrow）        ▏▏  ← 巨型│
│ │  章節大標題（88px）           ▏▏  數字  │
│ │  一句引言（italic 24px）       浮水印   │
│ │  ▢ SLIDES 03 — 11（range chip）        │
└────────────────────────────────────────┘
```
- 背景：`linear-gradient(135deg,#FFFFFF 0%,#FAF5F5 55%,#F4E5E6 100%)`
- `ch-bg-art`：420px 巨型章節數字浮水印，`color:rgba(183,40,46,0.07)`
- `ch-rule`：左側 6×140px 豎條，`linear-gradient(180deg,var(--red),var(--amber))`
- `ch-content`：垂直置中，`left:120px`

**規則**：章節大標統一**純色**（`var(--ink)`），不要逐字上色（已存在 `.accent` class 但 3 張章節頁都不該用——保持一致）。

---

## 5. 版面 Catalog（content-body 內的內容模式）

`content-body` 是 flex column。常見內容組合：

| 版型 | class | grid | 適用 |
|---|---|---|---|
| 開場引言 | `.concept-lead` | — | 每張內容頁第一段，italic Crimson 21px |
| 雙欄卡片 | `.vrmt-grid` | `1.05fr 1fr` | 兩塊對比卡片 |
| 圖文混排 | `.fda-grid` | `1.1fr 1fr` × 2 row | 截圖 + 說明 |
| 三步流程 | `.pipeline` | `1fr 28px 1fr 28px 1fr` | capture→mirror→render 類流程，中間夾箭頭 |
| 統計列 | `.stat-grid` | `repeat(4,1fr)` | 4 個並排數字 |
| why 補充條 | `.why-strip` | `auto repeat(3,1fr)` | 標籤 + 3 條佐證，淺底 |
| 深入比較 | `.sys-grid` / `.sys-card` | 雙欄 | 硬體／研究設計對照 |
| 圖表條 | `.sys-results` + inline `<svg>` | — | 底部長條圖／結果條 |
| 出處 | `.cite-line` | — | `margin-top:auto` 自動釘底 |

底部釘底技巧：`content-body > .cite-line{ margin-top:auto }` 讓出處永遠貼到可用區底部。內容會 overflow 時，改用 `.foot-stack`（絕對定位白底頁尾包住 eng-badge + cite-line）。

---

## 6. 可重用元件

### 6.1 `.card` — 標準資訊卡
```
border:1px solid var(--line) · border-radius:10px
padding:26px 30px 28px · box-shadow:0 14px 32px -22px rgba(20,30,60,.22)
```
組成：`.tag`（含 38×38 圓角 `.ico` 圖示）→ `h3` → `ul`（自訂圓點 bullet）→ `.footnote`（虛線上框）。
色彩變體：`.card.amber` / `.card.teal` — 換 tag 與 ico 的顏色。

### 6.2 `.concept-lead` — 開場引言
italic Crimson 21px。內嵌強調：
- `.accent` → 紅色非斜體粗體
- `.outcome` → teal + 螢光底線（`linear-gradient` 假底線）

### 6.3 `.eng-badge` — 技術規格條
monospace 12.5px，teal 左邊框 `border-left:3px solid var(--teal)`，淺 teal 底。開頭可放 `.label`（uppercase teal 小標）。

### 6.4 `.cite-line` — 參考文獻列
12.5px `var(--muted)`。`<b>` 內的作者名轉 `var(--ink-soft)`。中文人名引用採**連字號縮寫**（Hsu H-Y、Kuo L-C）。

### 6.5 footer-ribbon — 頁尾
固定元件，每張內容頁／章節頁都要有。複製整段即可，只改 `.pageno` 數字。

---

## 7. 色彩使用規則（重要慣例）

1. **紅 `--red` 是品牌主軸**：標題左邊框、footer、紅 tab、章節 rule、`.accent` 強調。
2. **teal `--teal` 只給「縮寫與技術名詞」**：標題裡的縮寫（VRMT、MT、ARMT）用 teal；`.outcome` 結果字也用 teal。標題其他字不要上 teal。
3. **amber `--amber` 是第三色**：卡片變體、章節漸層尾端。用量最少。
4. **同一張投影片強調色 ≤ 2 種**，避免花。
5. 章節大標**不上色**（純 `--ink`）。
6. 視覺裝飾要**對應講題的醫療次領域**（神經復健 deck 不要放心電圖等不相干圖示）。
7. 內文字級 **≥ 17pt**；可讀性優先於設計花俏。
8. 官方文件低解析截圖：保留截圖 + 在旁重打關鍵欄位；URL 放 cite 註腳，不放標題。

---

## 8. 製作與 QA 流程

1. **編輯**：直接改單一 `slides.html`（CSS 在 `<head>`，內容在各 `<section>`）。
2. **渲染**：headless Chrome 整捲截圖
   ```
   chrome --headless=new --disable-gpu --hide-scrollbars \
     --screenshot=full.png --window-size=1280,<40+N×752> \
     --virtual-time-budget=15000 slides.html
   ```
3. **切片**：PIL 以 `top=40, stride=752`（720 投影片 + 32 間距）逐張切出 1280×720。
4. **目檢**：做 contact sheet（6×6 縮圖）掃全局，再逐張看可疑頁。
5. **完整性稽核**：section IDs 連續、pageno 唯一連續、CSS 無 ghost selector、交叉引用指向有效頁。
6. 出貨：同步到 shipping 副本。

---

## 9. 已知陷阱（批次編輯時務必避開）

| # | 陷阱 | 對策 |
|---|---|---|
| 1 | SVG `<text>` 不支援 HTML 標籤 | 粗體用 `<tspan font-weight="700">`，**不要** `<b>/<i>` |
| 2 | 數字重編號的 regex 連鎖 | 由大到小取代，或用位置錨點逐一替換 |
| 3 | 插入／重排投影片 ID 撞號 | 兩階段 placeholder swap（`s28`→`__TMP_30__`→`s30`） |
| 4 | 交叉引用藏在 entity 裡 | 搜尋要含 `slide&nbsp;\d+`；跳過 CSS 註解 |
| 5 | **重編號後 CSS `#sN` selector 失效** | 投影片 ID 位移後，`#sN` 樣式規則沒跟著改 → 該頁版面崩。重編號時 section ID、pageno、**CSS selector**、cite 交叉引用四者要一起更新 |

> 第 5 點是 2026-05-19 的實戰教訓：插入 3 張章節分頁後，9 組 `#sN` CSS 規則指向錯誤投影片，導致 SM-ARMT 長條圖整個塌掉。

---

## 10. 新 deck 快速起手

1. 複製 `slides.html`，清空 `<body>` 內的 `<section>`，保留 `<head><style>` 整段。
2. 第一張用 `slide-title` 骨架（§4.1）。
3. 每個大段落前插一張 `chapter-break`（§4.3）。
4. 內容頁一律 `content-chrome` 骨架（§4.2）：page-head + content-body + footer-ribbon。
5. content-body 內依需求挑 §5 版型；元件用 §6。
6. 守 §7 色彩規則，跑 §8 QA，避開 §9 陷阱。
