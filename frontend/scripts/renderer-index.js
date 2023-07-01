const fileUpload = document.getElementById('formFileMultiple');
const viewPastScansButton = document.getElementById('viewPastScansButton');
const scanButton = document.getElementById('scanButton')
const processingList = document.getElementById('processingList')


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

window.electronAPI.updateScan((event, scanName)=> {
  let currentScanDiv = document.getElementById(scanName)
  processingList.removeChild(currentScanDiv)
  console.log("In scan update:"+scanName)
  showScan(scanName)
})

scanButton.addEventListener('click', () => {
  makeHttpCall(filesToScan)
  .then((response) => {
    console.log(`Response from HTTP was ${response}`)
    addNewScanToProcessingList(response)
  })
  reset_input()
})

viewPastScansButton.addEventListener('click', () => {
  window.electronAPI.changeView("pages/past-scans.html")
})

async function makeHttpCall(files) {
  let currDir = await window.electronAPI.sendRequest('http://127.0.0.1:5000/scan', files)
  filesToScan = []
  return currDir
}

function showScan(timestamp) {
  window.electronAPI.openNewWindow('pages/single-scan.html', [timestamp]);
}

function addNewScanToProcessingList(scanDir) {
  console.log("Adding new scan to the list")
  let wrapperDiv = document.createElement('div')
  wrapperDiv.setAttribute('id', scanDir)
  wrapperDiv.style.display = 'flex'

  let scanName = document.createElement('p')
  scanName.textContent = scanDir
  scanName.style.flex = '2'

  let spinner = document.createElement('div')
  spinner.classList.add('spinner-border')
  spinner.classList.add('text-primary')
  spinner.setAttribute('role', 'status')
  spinner.style.width='24px'
  spinner.style.height='24px'

  wrapperDiv.appendChild(scanName)
  wrapperDiv.appendChild(spinner)
  processingList.appendChild(wrapperDiv)
}

function reset_input() {
  fileUpload.value = null
  filesToScan = [];
  scanButton.disabled=true
}