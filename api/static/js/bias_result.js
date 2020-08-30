const myCanvas = document.getElementById('mycanvas');
const ctx = myCanvas.getContext("2d");
const indexnum = document.getElementById('index');

let index = 20;
//change index here


function componentToHex(c) {
  var hex = c.toString(16);
  return hex.length == 1 ? "0" + hex : hex;
}
function rgbToHex(r, g, b) {
  return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}

indexnum.innerText = index;

ctx.lineWidth = 5;
ctx.strokeStyle = rgbToHex(Math.floor(155*index/100)+100, Math.floor(155-155*index/100)+100, 0);
ctx.beginPath();
ctx.arc(75, 75, 50, -0.5*Math.PI, ((index/100) * 2 * Math.PI - 0.5*Math.PI));
ctx.stroke();
