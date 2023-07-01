const backButton = document.getElementById('backButton')
const ROOT_DIR = "C:\\Users\\aleks\\Projects\\IDC_Finder\\past_scans"

backButton.addEventListener('click', () => {
    window.electronAPI.changeView('pages/index.html', null);
})

window.addEventListener('load', () => {
    getPastScans(ROOT_DIR)
})

async function getPastScans(rootDir) {
    const receivedScanTimestamps = await window.electronAPI.getImages(rootDir)
    const pastScansHolder = document.getElementById('pastScansHolder')
    receivedScanTimestamps.forEach((scans) => {
        pastScansHolder.appendChild(createNewTileForImage(scans))
    })
}

function createNewTileForImage(scanTimestamp) {
    const previousScanHolder = document.createElement('div')
    previousScanHolder.addEventListener('click', () => showScan(scanTimestamp))
    previousScanHolder.classList.add('scan')
    previousScanHolder.innerText += scanTimestamp
    return previousScanHolder
}

function showScan(timestamp) {
    window.electronAPI.openNewWindow('pages/single-scan.html', [timestamp]);
}

