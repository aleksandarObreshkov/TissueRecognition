const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path')
const fs = require('fs')
const HOME_PAGE = 'pages/index.html'


function createWindow (htmlPage, args) {
  const mainWindow = new BrowserWindow({
    useContentSize: true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
    }
  })
  
  mainWindow.loadFile(htmlPage)
    .then(() => mainWindow.webContents.send("image-window-args", args))
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
  return fs.readdirSync(rootDir)
}

app.whenReady().then(() => {
  createWindow(HOME_PAGE, null);
  ipcMain.on('change-view', changeView);
  ipcMain.handle('read-files', readFiles)
  ipcMain.on('open-new-window', openNewWindow)

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