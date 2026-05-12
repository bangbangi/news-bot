const puppeteer = require("puppeteer");
const path = require("path");

(async () => {
  const inputHtml = process.argv[2] || "news_card.html";
  const outputPng = process.argv[3] || "news_card.png";

  const browser = await puppeteer.launch({
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 900, height: 1200 });

  const filePath = "file://" + path.resolve(inputHtml);
  await page.goto(filePath, { waitUntil: "networkidle0" });

  const card = await page.$(".card");
  if (!card) {
    throw new Error("캡처할 .card 요소를 찾을 수 없습니다.");
  }
  await card.screenshot({ path: outputPng });

  console.log(`${outputPng} 저장 완료`);
  await browser.close();
})();
