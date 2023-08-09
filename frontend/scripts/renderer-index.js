const fileUpload = document.getElementById('formFileMultiple');
const viewPastScansButton = document.getElementById('viewPastScansButton');
const scanButton = document.getElementById('scanButton')
const processingList = document.getElementById('processingList')
const alert_banner = document.getElementById('alert')
const alert_button = document.getElementById('alert-button')
const alert_message_holder = document.getElementById('error-message')
const processingArea = document.getElementById('processingArea')

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
  resetInput()
})

viewPastScansButton.addEventListener('click', () => {
  window.electronAPI.changeView("pages/past-scans.html")
})

window.electronAPI.receiveCurrentlyScanning((event, currentlyScanning) => {
  for (let scan of currentlyScanning) {
    addNewScanToProcessingList(scan)
  }
})

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

function createEye() {
  let eye = document.createElement('svg')
  eye.setAttribute('xmlns', "http://www.w3.org/2000/svg")
  eye.classList.add('bi','bi-eye', 'eye')


  eye.setAttribute('fill', 'currentColor')
  eye.setAttribute('viewBox', "0 0 16 16")

  let path1 = document.createElement('path')
  path1.setAttribute('d', "M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z")

  let path2 = document.createElement('path')
  path2.setAttribute('d', "M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z")


  eye.appendChild(path1)
  eye.appendChild(path2)

  return eye
}

function createScanNameParagraph(scanNameAndTimestamp) {
  let scanName = document.createElement('p')
  scanName.textContent = scanNameAndTimestamp
  scanName.style.verticalAlign = 'middle'
  scanName.style.flex = '2'
  scanName.style.display = 'flex'
  scanName.style.alignItems = 'center'
  scanName.style.marginBottom = '0'

  return scanName
}

function createScanSpinner(scanNameAndTimestamp) {
  let spinner = document.createElement('div')
  spinner.id = `${scanNameAndTimestamp}-spinner`
  spinner.classList.add('spinner-border')
  spinner.classList.add('text-primary')
  spinner.setAttribute('role', 'status')
  spinner.style.width='24px'
  spinner.style.height='24px'

  return spinner
}

function createOpenScanButton(scanTimestampAndName) {
  let img = document.createElement('img')
  img.style.width = '24px'
  img.style.height = '24px'
  img.src = '../resources/eye.svg'

  let seeScanButton = document.createElement('button');
  seeScanButton.id = `${scanTimestampAndName}-button`
  seeScanButton.classList.add('btn', 'btn-primary')
  seeScanButton.style.width = "fit-content"
  seeScanButton.style.height = "fit-content"

  seeScanButton.appendChild(img)
  seeScanButton.hidden = true
  seeScanButton.addEventListener('click', () => {
    let currentScanDiv = document.getElementById(scanTimestampAndName)
    processingList.removeChild(currentScanDiv)
    checkScanAreaEmpty()
    showScan(scanTimestampAndName)
  })

  return seeScanButton
}

function createScanWrapperDiv(scanNameAndTimestamp) {
  let wrapperDiv = document.createElement('div')
  wrapperDiv.setAttribute('id', scanNameAndTimestamp)
  wrapperDiv.style.display = 'flex'
  wrapperDiv.style.margin = '1px'

  return wrapperDiv
}