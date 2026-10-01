# WTMH Talk Template — 工作說明（給 Claude 的指南）

WTMH 實驗室演講投影片模板。1280×720 單檔 HTML deck，成大深紅品牌（`wtmh-design-kit/DESIGN-SYSTEM.md` 是設計法典，**風格不可偏離**）。範例成品：github.com/elfj/Madou_Sin-Lau_Hospital-20260723（線上 madou-sinlau-talk-2026.vercel.app）。

## 架構

- 內容寫在 `parts/sections-a~d.html`：每頁一個 `<section class="slide slide-title|content-chrome|chapter-break">`，頁尾寫 `<!--F:n-->` 巨集（n 隨便填，組裝時自動改對）
- `parts/build_deck.py` 組裝 `wtmh-design-kit/template.html` 的 head CSS＋全部 sections → `deck.html`，**自動重編 section id 與頁碼**，並注入播放模式（開站即單頁縮放、←→ 換頁、F 全螢幕、Esc 捲動總覽、`?scroll=1` 停用、`#N` 直達）
- `parts/make_print.py` → `deck-print.html`（剝掉播放器＋注入 @page 列印 CSS）
- `parts/shot.js` → `tmp/qa/full.png`（playwright 整卷截圖）；`parts/export_pdf.js` → `deck.pdf`

## 標準流程

```bash
npm install                      # 首次：裝 playwright-chromium
python parts/build_deck.py       # 組裝（看 stdout 的 sections 數與 ids sequential: True）
python parts/make_print.py
node parts/shot.js               # 整卷截圖 QA
# PIL 切片逐頁目檢：top=40+idx*752, 高720；重點頁必看
node parts/export_pdf.js         # 出 deck.pdf，用 pypdf 驗頁數
cp deck.html index.html          # Vercel 首頁
vercel deploy --prod --yes       # 部署（vercel link --yes --project <name> 先跑一次）
```

## 已知陷阱（實戰教訓，勿重蹈）

1. **章節分頁的 `Slides N — M` 是手寫的**——增刪頁後要手動更新每個 chapter-break 的 ch-range
2. **內容頁可用高度只有 474px**（top 138 / bottom 108，overflow:hidden 會裁）——cite-line 折兩行就會被切；寫完必渲染驗證
3. Windows headless Chrome 三坑：CJK 路徑的 file:// URL 要 EscapeUriString；`--screenshot` 會吃舊 user-data-dir 快取（改檔沒反應先懷疑這個）；`--print-to-pdf` 靜默失敗——**一律用 playwright（shot.js / export_pdf.js），不要直接呼叫 chrome.exe**
4. **Vercel 看到 package.json 會硬跑 build**——`.vercelignore` 已排除 package.json；`vercel.json` 設 framework null 純靜態，不要動
5. SVG 文字粗體用 `<tspan font-weight="700">`，不能用 `<b>`

## 內容慣例（學術演講標準）

- 每頁五要素：主題（h2）／內容／insight（concept-lead 開場＋bottomline-strip 收尾）／配圖或影片／cite-line 出處
- 網路圖片必標出處與日期；自製圖標「本演講自製」；影片頁放縮圖＋播放鍵＋連結印在圖說
- 數字誠實原則：媒體數字標「（案例報導值）」；未驗證指標標「（文獻報導範圍，非本系統驗證值）」；推估年限標「（研究推估，非承諾）」；成功率寫「8/8」不寫「100%」並帶條件
- 案例頁用「一個名字、一句話、一個數字」三段式；能力頁旁邊配「誠實邊界」頁
- 對抗式審查：可請 Codex 二審，但**只准建議內容/配圖/語氣/文字，不准動版面與風格**

## 起手式

新演講開工時：先跟用戶確認講題、場合日期、聽眾組成、頁數與 demo 安排，然後改 `sections-a.html` 的封面【】佔位，逐頁往下寫。素材放 `deck-assets/`。
