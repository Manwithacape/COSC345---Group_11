//  Create Camera Logic 
function createCamera(event) {
	event.preventDefault();
	const cameraName = document.getElementById("camera-name").value;
	const cameraMake = document.getElementById("camera-make").value;
	const cameraModel = document.getElementById("camera-model").value;
	const lensMake = document.getElementById("lens-make").value;
	const lensModel = document.getElementById("lensmodel").value;
	const aperture = document.getElementById("aperture").value;
	const shutterSpeed = document.getElementById("shutterspeed").value;
	const iso = document.getElementById("iso").value;
	const photoOfCamera = document.getElementById("photo-source").value;
	eel.create_camera(
		cameraName, cameraMake, cameraModel, lensMake, lensModel, aperture, shutterSpeed, iso, photoOfCamera 
	)(function(response) {
		if (response.success) {
			window.location.href = "dashboard.html";
}	
	});
}

function selectImage(selectionType = 'file'){
	eel.select_file(selectionType)(function(filePath) {
		document.getElementById("photo-of-camera").value = filePath;
		document.getElementById("photo-source").innerText = `Selected Image: ${filePath}`;
	});
}


window.addEventListener('DOMContentLoaded', () => {
    loadHeader();
    loadSidebar();

    // Setup sidebar resizer after sidebar loads
    setTimeout(setupSidebarResizer, 300); // Delay to ensure sidebar is loaded

    // Restore selectDirectory button functionality
    const selectImgButton = document.getElementById("photo-of-camera-btn");
    if (selectImgButton) {
        selectImgButton.addEventListener("click", () => {
            selectImage();
        });
    }

    // Restore sidebar toggle functionality
    const toggleSidebarBtn = document.getElementById("toggle-sidebar");
    if (toggleSidebarBtn) {
        toggleSidebarBtn.addEventListener("click", () => {
            toggleSidebar();
        });
    }

    eel.getallcollections()(collections => {
        if (Array.isArray(collections)) {
            loadCollectionCardsSequentially(collections);
        }
    });

    eel.onStart()(() => {
        const output = document.getElementById("output");
        if (output) output.innerText = "Application started successfully!";
    });
});
