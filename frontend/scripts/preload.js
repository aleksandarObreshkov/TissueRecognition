const { contextBridge, ipcRenderer } = require('electron')


contextBridge.exposeInMainWorld('electronAPI', {
  changeView: (htmlPage) => ipcRenderer.send('change-view', htmlPage),
  getImages: (rootDir) => ipcRenderer.invoke('read-files', rootDir),
  openNewWindow: (htmlPage, args) => ipcRenderer.send('open-new-window', htmlPage, args), 
  getArgs: (args) => ipcRenderer.on("image-window-args", args),
  sendRequestForScan: (body) => ipcRenderer.invoke('HTTP:send-request', body),
  updateScan: (scanName) => ipcRenderer.on('scan-update', scanName)
})