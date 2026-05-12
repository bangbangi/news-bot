const puppeteer = require("puppeteer");
const path = require("path");

(async () => {
  const browser = await puppeteer.launch({
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 900, height: 600 });

  const filePath = "file://" + path.resolve("news_card.html");
  await page.goto(filePath, { waitUntil: "networkidle0" });

  await page.screenshot({
    path: "news_card.png",
    fullPage: true,
  });

  console.log("news_card.png 저장 완료");
  await browser.close();
})();
