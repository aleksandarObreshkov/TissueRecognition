const { app, BrowserWindow, ipcMain, shell } = require('electron')
const path = require('path')
const fs = require('fs')
const HOME_PAGE = 'pages/index.html'
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));
const { exec } = require('node:child_process')
const express = require('express');
const BACKEND_URL = "http://127.0.0.1:5000"
//const ROOT_DIR = `${app.getAppPath()}\\dist\\server\\past_scans`
const ROOT_DIR = "C:\\Users\\aleks\\Projects\\IDC_Finder\\backend\\past_scans"

let currentScans = []

let  mainWindow;
let electronRestApi = express()
electronRestApi.use(express.json())

function removeScanFromCurrentScans(scan) {
  let index = currentScans.indexOf(scan)
  if (index == -1) {
    console.error("Error: Inconsistency. Trying to remove a scan which does not exist in frontend.")
    return null;
  }
  currentScans.splice(index, 1);
}

function createWindow (htmlPage, args) {
  let window = new BrowserWindow({
    height:800,
    width:1200,
    useContentSize: true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
    },
    show: true
  })
  
  window.loadFile(htmlPage)
    .then(() => window.webContents.send("image-window-args", args))
    .then(() => {
      if(args!=null) {
        window.setTitle(args[0])
      }
    })

  //window.removeMenu()
  return window
}

function closeAllWindows() {
  BrowserWindow.getAllWindows().forEach((w) => w.close())
}

function changeView(event, htmlPage) {
  const webContents = event.sender;
  const win = BrowserWindow.fromWebContents(webContents);
  win.loadFile(htmlPage)
}

function openNewWindow(event, htmlPage, args) {
  let newWindow = createWindow(htmlPage, args)
  newWindow.show()
}

function openFolder(event, folderName) {
  shell.openPath(`${ROOT_DIR}\\${folderName}`)
}

async function readFiles(event) {
  let dirs = fs.readdirSync(ROOT_DIR)
  let scansMap = new Map()
  for (let dir of dirs) {
    let files = fs.readdirSync(`${ROOT_DIR}\\${dir}`)
    scansMap.set(dir, files.length<2)
  }
  return scansMap
}

async function readResultImages(event, scanDir) {
  return [ROOT_DIR, fs.readdirSync(`${ROOT_DIR}\\${scanDir}`)]
}

async function sendRequestForScan(event, body) {
  try {
    let responseData = await fetch(`${BACKEND_URL}/scan`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body)
    });

    let status = responseData.status
    const expectedStatus = 201
    if(status != expectedStatus) {
      console.error(`Status was ${status}. Expected ${expectedStatus}`)
      throw new Error(responseData.body)
    }
  
    let scanDir = await responseData.text()
    currentScans.push(scanDir)
    return scanDir
  } catch(err) {
    console.error(`Error while sending scan request. Message: ${err}`)
    if(err.message.includes('SVS')){
      mainWindow.webContents.send('show-error-banner', err.message)
      return null
    }
    mainWindow.webContents.send('show-error-banner', "Error while sending scan request.")
    return null
  }
  
}

async function sendCloseSignalToServer() {
  try {
    const expectedStatus = 200
    const response = await fetch(`${BACKEND_URL}/quit`, {method: "POST"})
    if (response.status == expectedStatus) {
      closeAllWindows()
    }
    else {
      throw new Error(`Status was ${response.status}. Expected ${expectedStatus}`)
    }
  } catch(err) {
    console.error(`Error while trying to close the backend. Message: ${err}`)
    mainWindow.webContents.send('show-error-banner', "Could not close backend.")
  }
  
}

async function getCurrentlyScanning() {
  return currentScans
}

app.whenReady().then(() => {
  //exec(`start ${app.getAppPath()}\\dist\\server\\server.exe`); 

  mainWindow = createWindow(HOME_PAGE, null);
  ipcMain.on('change-view', changeView);
  ipcMain.handle('read-files', readFiles)
  ipcMain.handle('read-result-images', readResultImages)
  ipcMain.on('open-new-window', openNewWindow)
  ipcMain.handle('HTTP:send-request', sendRequestForScan)
  ipcMain.handle('currently-scanning', getCurrentlyScanning)
  ipcMain.on('open-folder', openFolder)

  electronRestApi.listen(5001, () => {
    console.log("Express is running on port 5001")
  })

  electronRestApi.post('/update', function(req, res) {
    let completedScanName = req.body.completedScan
    mainWindow.webContents.send('scan-update:SUCCESS', completedScanName)
    removeScanFromCurrentScans(completedScanName)
    res.sendStatus(200)
  })

  electronRestApi.post('/ready', function(req, res) {
    console.log("Backend ready")
    mainWindow.show()
    res.sendStatus(200)
  })

  electronRestApi.post('/failed', function(req, res) {
    let failedScanName = req.body.failedScan
    let exception = req.body.errorMessage

    console.log(`Scan ${failedScanName} failed.`)
    mainWindow.webContents.send('scan-update:ERROR', failedScanName, exception)
    removeScanFromCurrentScans(failedScanName)
    res.sendStatus(200)
  })

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow(HOME_PAGE, null)
  })

  mainWindow.on('close', () => {
    sendCloseSignalToServer()
  })
})

app.on('exit', () => {
  closeAllWindows()
})

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})