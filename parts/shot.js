// Full-page screenshot of deck.html via playwright-chromium
const path = require("path");
const { chromium } = require("playwright-chromium");

(async () => {
  const root = path.resolve(__dirname, "..");
  const browser = await chromium.launch({ executablePath: process.env.CHROME_PATH || undefined });
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  await page.goto("file:///" + root.replace(/\\/g, "/") + "/deck.html?scroll=1", { waitUntil: "networkidle" });
  await page.waitForTimeout(3000);
  await page.screenshot({ path: path.join(root, "tmp", "qa", "full.png"), fullPage: true });
  await browser.close();
  console.log("screenshot done");
})().catch((e) => { console.error(e); process.exit(1); });
