const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path')
const fs = require('fs')
const HOME_PAGE = 'pages/index.html'
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));
const { exec } = require('node:child_process')
const express = require('express');
const BACKEND_URL = "http://127.0.0.1:5000"

let  mainWindow;
let electron_rest_api = express()
electron_rest_api.use(express.json())

function createWindow (htmlPage, args) {
  let window = new BrowserWindow({
    height:650,
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
    return window
}

function closeAllWindows() {
  BrowserWindow.getAllWindows().forEach((w) => w.close())
}

function changeView(event, htmlPage) {
  const webContents = event.sender;
  const win = BrowserWindow.fromWebContents(webContents);
  win.loadFile(htmlPage);
}

function openNewWindow(event, htmlPage, args) {
  let newWindow = createWindow(htmlPage, args)
  newWindow.show()
}

async function readFiles(event, rootDir) {
  return fs.readdirSync(rootDir)
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
  
    const scanDir = await responseData.text()
    const status = responseData.status
    if(status!=202) {
      console.error(`Status was ${status}, but expected 202`)
      return null
    }
    return scanDir
  } catch(err) {
    console.error(`Error while sending scan request. Error: ${err}`)
    return null
  }
  
}

async function sendCloseSignalToServer() {
  const response = await fetch(`${BACKEND_URL}/quit`, {method: "POST"})
  if (response.status == 200) {
    closeAllWindows()
  }
}

app.whenReady().then(() => {
  //exec(`start ${app.getAppPath()}\\dist\\server\\server.exe`); 


  mainWindow = createWindow(HOME_PAGE, null);
  ipcMain.on('change-view', changeView);
  ipcMain.handle('read-files', readFiles)
  ipcMain.on('open-new-window', openNewWindow)
  ipcMain.handle('HTTP:send-request', sendRequestForScan)

  electron_rest_api.listen(5001, () => {
    console.log("Express is running on port 5001")
  })

  electron_rest_api.post('/update', function(req, res) {
    let completedScanName = req.body.completedScan
    mainWindow.webContents.send('scan-update', completedScanName)
    res.sendStatus(200)
  })

  electron_rest_api.post('/ready', function(req, res) {
    console.log("Backend ready")
    mainWindow.show()
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