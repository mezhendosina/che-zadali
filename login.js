const python = require('python-shell');
const puppeteer = require('puppeteer');  ///setup browser
SGO_LOGIN = 'МеньшенинЕ1';
SGO_PASSWORD = '787970';

async function homework(){
  const url = 'https://sgo.edu-74.ru/'
  const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setCookie({
      url: url,
      name: 'TTSLogin',
      value: 'SCID=89&PID=-1&CID=2&SID=1&SFT=2&CN=1&BSP=0'
  });
  ///go to sgo.edu-74.ru
  await console.log('go to sgo.edu-74.ru')
  await page.goto(url, { waitUntil: 'networkidle2' });
  
  await page.waitForTimeout(3000); /// wait

  ///type login/password
  await console.log('type loginlo')
  await page.$eval(
    '#message > div > div > div:nth-child(8) > input', 
    (el, value) => el.value = value, 
    SGO_LOGIN);
  await console.log('type password')
  await page.$eval(
    '#message > div > div > div:nth-child(9) > input',
    (el, value) => el.value = value,
    SGO_PASSWORD
    );

  ///click login button
  await console.log('click login button')
  await page.click('#message > div > div > div:nth-child(11) > a > span');

  await page.waitForTimeout(5000); ///wait

  //Security warn
  try{
      await page.click(
        'body > div.block-content > div > div > div > div > div:nth-child(5) > div > div > div > div > button:nth-child(2)'
        )
      await console.log('Access is allowed🔓')
  }
  catch(e){
      await console.log('Security warn is not found😒')
  }

  await page.waitForTimeout(10000); ///wait
  
  for(let i = 0;i <10;i++ ){
      await page.click('#view > div:nth-child(5) > div > div > div.schooljournal_content.column > div.controls_box > div.week_switcher > div.button_prev > i')
      await page.waitForTimeout(1000); ///wait
  }
  await page.waitForTimeout(3000); ///wait

  const content = page.content(); /// get page content
/*
  ///logout
  try{
  await page.click('body > div.header > div.block-personal-cabinet > ul > li.no_separator > a')
  await page.waitForTimeout(1000); ///wait
  await page.click('#\34 cb4019b-01bb-423d-9a43-a10d2ec9259e > span')
  }
  catch(e){
      console.log(':(')
  }
  await browser.close();
  */ 
  const { spawn } = require('child_process');
  const pyProg = spawn('python', ["extractHomeworkFromHTML.py", content]);
  pyProg.stdout.on('data', function(data) {
    console.log('done')
  })
}
let h = homework()
console.log(h)