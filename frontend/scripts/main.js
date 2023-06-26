const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path')
const fs = require('fs')
const HOME_PAGE = 'pages/index.html'
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));
const { exec } = require('node:child_process');


function createWindow (htmlPage, args) {
  const mainWindow = new BrowserWindow({
    useContentSize: true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
    }
  })
  
  mainWindow.loadFile(htmlPage)
    .then(() => mainWindow.webContents.send("image-window-args", args))
    .then(() => {
      if(args!=null) {
        mainWindow.setTitle(args[0])
      }
    })
    .then(() => mainWindow.show())
}

function changeView(event, htmlPage) {
  const webContents = event.sender;
  const win = BrowserWindow.fromWebContents(webContents);
  win.loadFile(htmlPage);
}

function openNewWindow(event, htmlPage, args) {
  createWindow(htmlPage, args)
}

async function readFiles(event, rootDir) {
  console.log(rootDir)
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
  const responseJson = await responseData.text()
  return responseJson
}

app.whenReady().then(() => {
  exec(`start ${app.getAppPath()}\\dist\\server\\server.exe`); 

  createWindow(HOME_PAGE, null);
  ipcMain.on('change-view', changeView);
  ipcMain.handle('read-files', readFiles)
  ipcMain.on('open-new-window', openNewWindow)
  ipcMain.handle('HTTP:send-request', sendRequest)

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow(HOME_PAGE, null)
  })
})

app.on('exit', () => {
  BrowserWindow.getAllWindows().forEach((w) => w.close())
})

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})