const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path')
const fs = require('fs')
const HOME_PAGE = 'pages/index.html'
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));
const { exec } = require('node:child_process')
const express = require('express');

let  mainWindow;
let api = express()
api.use(express.json())

function createWindow (htmlPage, args) {
  let window = new BrowserWindow({
    height:650,
    width:1200,
    useContentSize: true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
    },
    //show: false
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

async function sendRequest(event, url, body) {
  let responseData = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body)
  });
  const scanDir = await responseData.text()
  const status = responseData.status
  if(status != 202) {
    console.log("Something went wrong")
  }
  return scanDir
}

app.whenReady().then(() => {
  //exec(`start ${app.getAppPath()}\\dist\\server\\server.exe`); 


  mainWindow = createWindow(HOME_PAGE, null);
  ipcMain.on('change-view', changeView);
  ipcMain.handle('read-files', readFiles)
  ipcMain.on('open-new-window', openNewWindow)
  ipcMain.handle('HTTP:send-request', sendRequest)

  api.listen(5001, () => {
    console.log("Express is running on port 5001")
  })

  api.post('/update', function(req, res) {
    let completedScanName = req.body.completedScan
    mainWindow.webContents.send('scan-update', completedScanName)
    res.sendStatus(200)
  })

  api.post('/ready', function(req, res) {
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

function closeAllWindows() {
  BrowserWindow.getAllWindows().forEach((w) => w.close())
}

async function sendCloseSignalToServer() {
  const response = await fetch('http://127.0.0.1:5000/quit', {method: "POST"})
  if (response.status == 200) {
    closeAllWindows()
  }
}