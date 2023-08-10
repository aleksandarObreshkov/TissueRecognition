const fileUpload = document.getElementById('formFileMultiple');
const viewPastScansButton = document.getElementById('viewPastScansButton');
const scanButton = document.getElementById('scanButton')
const processingList = document.getElementById('processingList')
const alert_banner = document.getElementById('alert')
const alert_button = document.getElementById('alert-button')
const alert_message_holder = document.getElementById('error-message')
const processingArea = document.getElementById('processingArea')

let filesToScan = []

window.addEventListener('load', () => {
  getCurrentScans()
})

async function getCurrentScans() {
  let scans = await window.electronAPI.getCurrentlyScanning()
  console.log(scans)

  for (let scan of scans) {
    addNewScanToProcessingList(scan)
  }
}

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
  resetInput()
})

viewPastScansButton.addEventListener('click', () => {
  window.electronAPI.changeView("pages/past-scans.html")
})

// window.electronAPI.receiveCurrentlyScanning((event, currentlyScanning) => {
//   for (let scan of currentlyScanning) {
//     addNewScanToProcessingList(scan)
//   }
// })

window.electronAPI.updateScan((event, scanNameAndTimestamp) => {
  console.log(`In scan update: ${scanNameAndTimestamp}`)
  showScanOpenButton(scanNameAndTimestamp)
})

window.electronAPI.errorScan((event, scanNameAndTimestamp, errorMessage) => {
  console.log(`In scan error: ${scanNameAndTimestamp}. Error message: ${errorMessage}`)
  let currentScanDiv = document.getElementById(scanNameAndTimestamp)
  let imageName = scanNameAndTimestamp.substring(scanNameAndTimestamp.indexOf("-")+1) //removes the timestamp from the name
  displayAlertWithMessage(`Scanning of image ${imageName} failed. Reason: ${errorMessage}`)
  processingList.removeChild(currentScanDiv)
  checkScanAreaEmpty()
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

function addNewScanToProcessingList(scanTimestampAndName) {
  console.log(`Adding new scan to the list: ${scanTimestampAndName}`)

  let wrapperDiv = createScanWrapperDiv(scanTimestampAndName)
  let scanNameParagraph = createScanNameParagraph(scanTimestampAndName)
  let scanSpinner = createScanSpinner(scanTimestampAndName)
  let openScanButton = createOpenScanButton(scanTimestampAndName)

  wrapperDiv.appendChild(scanNameParagraph)
  wrapperDiv.appendChild(scanSpinner)
  wrapperDiv.appendChild(openScanButton)

  processingList.appendChild(wrapperDiv)
  checkScanAreaEmpty()
}

function showScanOpenButton(scanName) {
  let openScanButton = document.getElementById(`${scanName}-button`)
  let loadingScanSpinner = document.getElementById(`${scanName}-spinner`)

  openScanButton.hidden = false
  loadingScanSpinner.hidden = true
}

function resetInput() {
  fileUpload.value = null
  filesToScan = [];
  scanButton.disabled=true
}

function displayAlertWithMessage(message) {
  alert_message_holder.textContent = message
  alert_banner.hidden = false
}

function checkScanAreaEmpty() {
  if (processingList.children.length == 0) {
    processingArea.hidden = true
  }

  if (processingList.children.length > 0) {
    processingArea.hidden = false
  } 
}

function createScanNameParagraph(scanNameAndTimestamp) {
  let scanName = document.createElement('p')
  scanName.textContent = scanNameAndTimestamp
  scanName.classList.add('scan-paragraph')

  return scanName
}

function createScanSpinner(scanNameAndTimestamp) {
  let spinner = document.createElement('div')
  spinner.id = `${scanNameAndTimestamp}-spinner`
  spinner.classList.add('spinner-border', 'text-primary', 'scan-spinner')
  spinner.setAttribute('role', 'status')

  return spinner
}

function createOpenScanButton(scanTimestampAndName) {
  let eye = createEyeImg()

  let seeScanButton = document.createElement('button');
  seeScanButton.id = `${scanTimestampAndName}-button`
  seeScanButton.classList.add('btn', 'btn-primary', 'eye-button')

  seeScanButton.appendChild(eye)
  seeScanButton.hidden = true

  seeScanButton.addEventListener('click', () => {
    let currentScanDiv = document.getElementById(scanTimestampAndName)
    processingList.removeChild(currentScanDiv)
    checkScanAreaEmpty()
    showScan(scanTimestampAndName)
  })

  return seeScanButton
}

function createEyeImg() {
  let img = document.createElement('img')
  img.classList.add('scan-img')
  img.src = '../resources/eye.svg'

  return img
}

function createScanWrapperDiv(scanNameAndTimestamp) {
  let wrapperDiv = document.createElement('div')
  wrapperDiv.classList.add('scan-wrapper')
  wrapperDiv.setAttribute('id', scanNameAndTimestamp)

  return wrapperDiv
}