# WTMH Talk Template

WTMH 實驗室演講投影片模板：1280×720 WTMH 深紅設計系統＋自動組裝管線＋內建播放模式＋PDF 匯出＋Vercel 靜態部署。

## 快速開始

1. GitHub 按 **Use this template** 開新 repo（一場演講一個 repo）
2. `npm install`
3. 編輯 `parts/sections-*.html`（範例骨架在 sections-a.html）
4. `python parts/build_deck.py` → 開 `deck.html` 即可播放（←→ 換頁、F 全螢幕、Esc 總覽）
5. 匯 PDF：`python parts/make_print.py && node parts/export_pdf.js`
6. 部署：`cp deck.html index.html && vercel deploy --prod --yes`

詳細工作流程、設計規範與陷阱清單見 `CLAUDE.md` 與 `wtmh-design-kit/DESIGN-SYSTEM.md`。

範例成品：[Madou_Sin-Lau_Hospital-20260723](https://github.com/elfj/Madou_Sin-Lau_Hospital-20260723)（[線上版](https://madou-sinlau-talk-2026.vercel.app)）
