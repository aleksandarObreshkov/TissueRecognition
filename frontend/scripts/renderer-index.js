const fileUpload = document.getElementById('formFileMultiple');
const viewPastScansButton = document.getElementById('viewPastScansButton');
const scanButton = document.getElementById('scanButton')
const processingList = document.getElementById('processingList')
const alert_banner = document.getElementById('alert')
const alert_button = document.getElementById('alert-button')
const alert_message_holder = document.getElementById('error-message')

let filesToScan = []

alert_button.addEventListener('click', () => {
  alert_banner.hidden = true
})

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
  makeHttpCall(filesToScan)
  .then((response) => {
    if (response!=null) {
      console.log(`Response from HTTP was ${response}`)
      addNewScanToProcessingList(response)
    }
  })
  reset_input()
})

viewPastScansButton.addEventListener('click', () => {
  window.electronAPI.changeView("pages/past-scans.html")
})

window.electronAPI.updateScan((event, scanName)=> {
  let currentScanDiv = document.getElementById(scanName)
  processingList.removeChild(currentScanDiv)
  console.log("In scan update:"+scanName)
  showScan(scanName)
})

window.electronAPI.showErrorBanner((event, err) => {
  console.log(err)
  displayAlertWithMessage(err)
})

async function makeHttpCall(files) {
  let currDir = await window.electronAPI.sendRequestForScan(files)
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

function displayAlertWithMessage(message) {
  alert_message_holder.textContent = message
  alert_banner.hidden = false
}