const fileUpload = document.getElementById('formFileMultiple');
const viewPastScansButton = document.getElementById('viewPastScansButton');
const scanButton = document.getElementById('scanButton')


let filesToScan = []

fileUpload.addEventListener('change', () => {
  const files = fileUpload.files
  if(files!=null) {
    scanButton.disabled = false
  }
  // Loop through files
  for (let i = 0; i < files.length; i++) {
    filesToScan.push(files.item(i).path)
  }
})

scanButton.addEventListener('click', () => {
  makeHttpCall(filesToScan).then((response) => {
    console.log(`Response from HTTP was ${response}`)
    showScan(response)
  })
  reset_input()
})

viewPastScansButton.addEventListener('click', () => {
  window.electronAPI.changeView("pages/pastScans.html")
})

async function makeHttpCall(files) {
  let response = await window.electronAPI.sendRequest('http://127.0.0.1:5000/scan', files)
  filesToScan = []
  return response
}

function showScan(timestamp) {
  window.electronAPI.openNewWindow('pages/singleScan.html', [timestamp]);
}

function reset_input() {
  fileUpload.value = null
  filesToScan = [];
  scanButton.disabled=true
}