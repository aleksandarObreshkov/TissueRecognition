const rootCarousel = document.getElementById('carouselInner')

window.addEventListener('load', () => window.electronAPI.getArgs((_event, args) => {
    createImages(args)
}))

async function createImages(scanNameWithTimestamp) {
    let [rootDir, receivedImages] = await window.electronAPI.getResultImages(scanNameWithTimestamp[0])
    let counter = 0
    receivedImages.forEach((scan) => {
        let carouselImageDiv = document.createElement('div')
        carouselImageDiv.classList.add('carousel-item')
        if(counter==0) carouselImageDiv.classList.add('active')
        counter +=1

        let carouselImage = document.createElement('img')
        let carouselImageDir = rootDir + '\\' + scanNameWithTimestamp + "\\" + scan
        carouselImage.classList.add('d-block')
        carouselImage.classList.add('w-100')
        carouselImage.classList.add('carousel-image')
        carouselImage.setAttribute('src', carouselImageDir)

        carouselImageDiv.appendChild(carouselImage)

        rootCarousel.appendChild(carouselImageDiv)
    })
}