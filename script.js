const { Builder, By, Key, util } = require("selenium-webdriver");
const webdriver = require("selenium-webdriver");
const chrome = require("selenium-webdriver/chrome");
const chromedriver = require("chromedriver");

chrome.setDefaultService(new chrome.ServiceBuilder(chromedriver.path).build());

function get_alt(line) {
  const str = '//img[@alt="' + line + '"]';
  return str;
}

var driver = new webdriver.Builder()
  .withCapabilities(webdriver.Capabilities.chrome())
  .build();

lines = { "A line": "A", "B line": "B", "C line": "C" };

async function open_omny() {
  await driver.get("https://omny.info/schedules/new-york-city-subway");
}

async function iterate_line(line) {
  console.log(line);

  script =
    "return window.getComputedStyle(document.querySelector('.span'),'::before').getPropertyValue('content')";

  var element = driver.executeScript(script);

  element.then(function (text) {
    console.log(text);
  });
}

async function iterate_lines() {
  for (var key in lines) {
    console.log(get_alt(key));
    await driver.findElement(By.xpath(get_alt(key))).click();
    await iterate_line(lines[key]);
    await open_omny();
  }
}

open_omny();
iterate_lines();
