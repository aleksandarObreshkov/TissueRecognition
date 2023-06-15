const fileUpload = document.getElementById('formFileMultiple');
const viewPastScansButton = document.getElementById('viewPastScansButton');

fileUpload.addEventListener('change', () => {
  const files = fileUpload.files

  // Loop through files
  for (let i = 0; i < files.length; i++) {
    let file = files.item(i)
    console.log(file.path)
  }
  
})

viewPastScansButton.addEventListener('click', () => {
  console.log("Im here")
  window.electronAPI.changeView("pages/pastScans.html")
})