# WTMH Design Kit

WTMH 實驗室共用簡報設計風格 + 通用底圖,打包成單一資料夾,方便之後任何新專案直接拿來用。

> 設計系統最早從 VRMT 神經復健研究簡報(34 張)萃取,已驗證跨 VRMT / ECG / Sleep 三組可沿用。

## 資料夾結構

```
wtmh-design-kit/
├── README.md             ← 這份檔案(快速上手)
├── DESIGN-SYSTEM.md      ← 完整設計系統規格(色彩 token、字體階層、版面 catalog、5 個編輯陷阱)
├── template.html         ← 空白 HTML 骨架(內含完整 design system CSS + 6 種示範版型)
├── assets/
│   ├── brand/            ← 校徽 / 實驗室 / 學會 logo(每張簡報都會用到)
│   │   ├── logo-ncku-h-small.png        footer-ribbon 用的 NCKU 橫式小 logo
│   │   ├── logo-ncku-seal.png           封面用的 NCKU 校徽
│   │   ├── logo-wtmh-new-small.png      footer-ribbon 用的 WTMH 圓形小 logo
│   │   ├── logo-wtmh-new-clean.png      WTMH 完整版(較大)
│   │   ├── logo-ifmbe.png               IFMBE 學會 logo
│   │   └── logo-mdi.png                 醫療器材創新中心 MDI logo
│   └── headers/          ← title slide 頂部裝飾橫幅(`.top-deco`)
│       ├── header-full.png              完整橫幅(預設)
│       ├── header-deco.png              裝飾版
│       ├── header-left.png              左半段
│       └── header-right.png             右半段
└── examples/             ← 最終成品(設計風格實際長相)
    ├── wtmh-vrmt-only.html              純 VRMT 簡報 34 張
    ├── wtmh-vrmt-only.pdf
    ├── wtmh-lab-portfolio.html          完整實驗室組合 53 張(VRMT + ECG + Sleep)
    └── wtmh-lab-portfolio.pdf
```

## 怎麼用(新專案三步)

### 1. 複製 `template.html` 改名成你的 deck
```bash
cp template.html my-new-deck.html
```
打開它你會看到 6 種版型示範:封面、章節分頁、雙欄卡片、三步流程、四格數字、結語。

### 2. footer logo 替換為實際檔案
template.html 的 footer 預設是註解,把它換成真的 `<img>`:
```html
<div class="fl-left">
  <img class="ncku-logo" src="assets/brand/logo-ncku-h-small.png" alt="NCKU" />
  <img class="wtmh-logo" src="assets/brand/logo-wtmh-new-small.png" alt="WTMH Lab" />
</div>
```

### 3. 封面 logo / 主視覺
封面 `slide-title` 的 hero-art 用 brand logo 或自製主視覺;`title-foot` 放夥伴 logo(IFMBE、MDI、NCKU seal)。

## 設計鐵則(摘自 DESIGN-SYSTEM.md)

| 規格 | 值 |
|---|---|
| 畫布 | **1280 × 720 px**(16:9,固定) |
| 內容頁可用高度 | **474 px**(720 − 138 header − 108 footer)— 超出會被 `overflow:hidden` 裁掉 |
| 字體 | 標題 Crimson Pro · 內文 Inter · 中文 Noto Sans / Noto Serif TC |
| 主色 | 紅 `#B7282E` · teal `#0E9FBA`(只給縮寫)· amber `#D96A18` |
| 強調色 | 一張投影片 ≤ 2 種 |
| 裝飾圖 | 必須對應主題的醫療次領域(神經復健 deck 不要放心電圖等) |

## HTML → PDF 轉檔

範例 PDF 是用 headless Chrome `--print-to-pdf` 加上 `@media print` CSS 注入產生的。完整腳本見 `wtmh-deck-template` repo 內的 `_html_to_pdf.py`。

```bash
chrome --headless=new --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=my-deck.pdf --virtual-time-budget=20000 \
  file:///path/to/my-deck.html
```
(每張投影片 = 一頁 PDF,需事先注入 `@page { size: 1280px 720px; margin: 0 }` + `.slide { page-break-after: always }`)

## 相關 repo / 檔案

- GitHub: `github.com/elfj/wtmh-deck-template`(Private)— design system code repo,有 `_build_*.py` 產生器、ECG / Sleep 範例 part、`_html_to_pdf.py` 等。
- 來源:VRMT 簡報 `html_rebuild/out/slides.html`(NCKU WTMH Lab)。
- 萃取日期:2026-05-21。
