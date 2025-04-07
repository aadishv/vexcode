const takeStep = (f) => {
  const classname = "vcj action_btn blue blocky  active ";
  if (document.getElementsByClassName(classname).length == 2) {
    document.getElementsByClassName(classname)[1].click();
  }
  f();
}
function getElementByInnerText(text) {
  return Array.from(document.querySelectorAll('*'))
    .find(element => element.textContent.trim() === text);
}
// JavaScript equivalent to simulate keypresses in a browser environment
function simulateKeyPress(key) {
  const event = new KeyboardEvent('keydown', { key: key, bubbles: true });
  document.activeElement.dispatchEvent(event);
}

document.getElementById('top_config_button').click();
document.getElementsByClassName("card_row flex_row justify_space_between")[0].click();
getElementByInnerText("AI VISION").click();
document.getElementsByClassName("port_select_btn flex_column ")[0].click();
getElementByInnerText("Configure").click();
document.getElementsByClassName("rc flat blue active ")[0].click();
document.getElementsByClassName("toggle_slider")[1].click();
(async function () { await new Promise(r => setTimeout(r, 700)); })();
console.log(document.getElementsByClassName("connectVideoBtn")[0].click(), "hello")
document.getElementsByClassName("connectVideoBtn")[0].click();
(async function () { await new Promise(r => setTimeout(r, 700)); })();
