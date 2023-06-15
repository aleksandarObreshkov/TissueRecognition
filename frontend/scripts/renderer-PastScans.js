const backButton = document.getElementById('backButton')

backButton.addEventListener('click', ()=> {
    window.electronAPI.changeView('pages/index.html');
})

window.addEventListener('load', () => {
    displayImages("C:\\Users\\aleks\\Desktop\\image\\testing")
})

async function displayImages(rootDir) {
    const receivedImages = await window.electronAPI.getImages(rootDir)
    const imageHolder = document.getElementById('imageHolder')
    for (let imagePath of receivedImages) {
        const image = document.createElement('img')
        let fullImagePath = rootDir+'\\'+imagePath
        console.log(fullImagePath)
        image.setAttribute('src', fullImagePath)
        imageHolder.appendChild(image)
    }
}

