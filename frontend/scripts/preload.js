const { contextBridge, ipcRenderer } = require('electron')


contextBridge.exposeInMainWorld('electronAPI', {
  changeView: (htmlPage) => ipcRenderer.send('change-view', htmlPage),
  getImages: () => ipcRenderer.invoke('read-files'),
  getResultImages: (scanDir) => ipcRenderer.invoke('read-result-images', scanDir),
  openNewWindow: (htmlPage, args) => ipcRenderer.send('open-new-window', htmlPage, args), 
  getArgs: (args) => ipcRenderer.on("image-window-args", args),
  sendRequestForScan: (body) => ipcRenderer.invoke('HTTP:send-request', body),
  updateScan: (scanName) => ipcRenderer.on('scan-update:SUCCESS', scanName),
  errorScan:(scanName, errorMessage) => ipcRenderer.on('scan-update:ERROR', scanName, errorMessage),
  showErrorBanner: (error) => ipcRenderer.on('show-error-banner', error),
  getCurrentlyScanning: () => ipcRenderer.invoke('currently-scanning'),
  openFolder: (timestamp) => ipcRenderer.send('open-folder', timestamp)
})