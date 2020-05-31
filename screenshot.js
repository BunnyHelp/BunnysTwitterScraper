const puppeteer = require('puppeteer');

var fs = require('fs');
var URL = fs.readFileSync('temp.txt','utf8');


(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
    await page.setViewport({
	  width: 1200,
	  height: 4000,
	  deviceScaleFactor: 1.5,
  });
  await page.goto(URL);
  await page.waitFor(3000);
  await page.screenshot({path: 'screenshot.png'});
  await browser.close();
})();