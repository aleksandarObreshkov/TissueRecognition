const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electronAPI', {
  changeView: (htmlPage) => ipcRenderer.send('change-view', htmlPage),
  getImages: (rootDir) => ipcRenderer.invoke('read-files', rootDir)
})