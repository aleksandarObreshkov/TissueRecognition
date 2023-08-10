const backButton = document.getElementById('backButton')
const ROOT_DIR = "C:\\Users\\aleks\\Projects\\IDC_Finder\\past_scans"

backButton.addEventListener('click', () => {
    window.electronAPI.changeView('pages/index.html', null);
})

window.addEventListener('load', () => {
    getPastScans(ROOT_DIR)
})

window.electronAPI.updateScan((event, scanNameAndTimestamp) => {
    console.log(`In scan update in past scans: ${scanNameAndTimestamp}`)
    let eyeButton = document.getElementById(`${scanNameAndTimestamp}-eye-button`)
    let folderButton = document.getElementById(`${scanNameAndTimestamp}-folder-button`)
    eyeButton.disabled = false
    folderButton.disabled = false
})

async function getPastScans(rootDir) {
    const receivedScanTimestamps = await window.electronAPI.getImages(rootDir)
    const pastScansHolder = document.getElementById('scansHolder')

    for (const [key, value] of receivedScanTimestamps) {
        pastScansHolder.appendChild(createNewRowForImage(key, value))
    }
}

function createNewRowForImage(scanTimestamp, isReady) {
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
    const filenameColumn = document.createElement('td')
    const dateColumn = document.createElement('td')
    const actionsColumn = document.createElement('td')

    let eye = document.createElement('img')
    eye.style.width = '20px'
    eye.style.height = '20px'
    eye.src = '../resources/eye.svg'

    const openButton = document.createElement("button")
    openButton.classList.add('btn', 'btn-primary', 'eye-button')
    openButton.id = `${scanTimestamp}-eye-button`
    openButton.appendChild(eye)
    openButton.addEventListener('click', () => showScan(scanTimestamp))
    openButton.disabled = isReady

    let folder = document.createElement('img')
    folder.style.width = '20px'
    folder.style.height = '20px'
    folder.src = '../resources/folder.svg'

    const folderButton = document.createElement("button")
    folderButton.classList.add('btn', 'btn-secondary', 'eye-button')
    folderButton.id = `${scanTimestamp}-folder-button`
    folderButton.appendChild(folder)
    folderButton.addEventListener('click', () => openFolder(scanTimestamp))
    folderButton.disabled = isReady

    let buttonHolder = document.createElement('div')
    buttonHolder.classList.add('actions-button-holder')
    buttonHolder.appendChild(openButton)
    buttonHolder.appendChild(folderButton)

    filenameColumn.textContent = file_name
    dateColumn.textContent = `${day}.${month}.${year} ${hour}:${minutes}:${secs}`

    actionsColumn.appendChild(buttonHolder);



    row.appendChild(filenameColumn)
    row.appendChild(dateColumn)
    row.appendChild(actionsColumn)
    return row
}

function showScan(timestamp) {
    window.electronAPI.openNewWindow('pages/single-scan.html', [timestamp]);
}

function openFolder(timestamp) {
    window.electronAPI.openFolder(timestamp)
}

