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
    const pastScansHolder = document.getElementById('scansHolder')
    receivedScanTimestamps.forEach((scans) => {
        pastScansHolder.appendChild(createNewRowForImage(scans))
    })
}

function createNewRowForImage(scanTimestamp) {
    const re = /(\d{8})T(\d{6})-(\w+)/
    const match = scanTimestamp.match(re);
    let date = match[1]
    let time = match[2]
    let file_name = match[3]

    let year = date.slice(0, 4)
    let month = date.slice(4, 6)
    let day = date.slice(6, 8)

    let hour = time.slice(0,2)
    let minutes = time.slice(2, 4)
    let secs = time.slice(4, 6)

    const row = document.createElement('tr')
    const filename_col = document.createElement('td')
    const date_col = document.createElement('td')
    const actions_col = document.createElement('td')

    const openButton = document.createElement("button")
    openButton.classList.add('btn', 'btn-primary')
    openButton.textContent = "Open scan";
    openButton.addEventListener('click', () => showScan(scanTimestamp))

    filename_col.textContent = file_name
    date_col.textContent = `${day}.${month}.${year} ${hour}:${minutes}:${secs}`
    console.log(date_col.textContent)
    actions_col.appendChild(openButton);

    row.appendChild(filename_col)
    row.appendChild(date_col)
    row.appendChild(actions_col)
    return row
}

function showScan(timestamp) {
    window.electronAPI.openNewWindow('pages/single-scan.html', [timestamp]);
}

