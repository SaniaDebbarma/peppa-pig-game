let count = 0

function updateUI() {
  document.getElementById("count").innerText = count
}

function increase() {
  count++
  updateUI()
}

function decrease() {
  count--
  updateUI()
}

function reset() {
  count = 0
  updateUI()
}