// Export deck-print.html to PDF via playwright-chromium
const path = require("path");
const { chromium } = require("playwright-chromium");

(async () => {
  const root = path.resolve(__dirname, "..");
  const browser = await chromium.launch({ executablePath: process.env.CHROME_PATH || undefined });
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  await page.goto("file:///" + root.replace(/\\/g, "/") + "/deck-print.html", { waitUntil: "networkidle" });
  await page.waitForTimeout(3000); // webfonts
  await page.pdf({
    path: path.join(root, "deck.pdf"),
    width: "1280px",
    height: "720px",
    printBackground: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 },
  });
  await browser.close();
  console.log("PDF exported");
})().catch((e) => { console.error(e); process.exit(1); });
