// CameraCreation.js

function createCamera(event) {
  event.preventDefault();
  const cameraName   = document.getElementById("camera-name").value.trim();
  const cameraMake   = document.getElementById("camera-make").value.trim();
  const cameraModel  = document.getElementById("camera-model").value.trim();
  const lensMake     = document.getElementById("lens-make").value.trim();
  const lensModel    = document.getElementById("lens-model").value.trim();
  const aperture     = document.getElementById("aperture").value.trim();
  const shutterSpeed = document.getElementById("shutter-speed").value.trim();
  const iso          = document.getElementById("iso").value.trim();
  const photoOfCamera= document.getElementById("photo-source").value || null;

  eel.create_camera(
    cameraName, cameraMake, cameraModel, lensMake, lensModel,
    aperture, shutterSpeed, iso, photoOfCamera
  )((resp) => {
    if (resp && resp.success) {
      // optionally show success and stay on page
      // window.location.href = "dashboard.html";
      alert(`Saved camera: ${resp.camera.camera_name}`);
    } else {
      alert("Failed to save camera");
    }
  });
}

function selectImage(selectionType = 'file'){
  eel.select_file(selectionType)((filePath) => {
    if (!filePath) return;
    document.getElementById("photo-source").value = filePath;               // store for submit
    document.getElementById("photo-of-camera-btn").textContent = "✓ Image selected";
  });
}

window.addEventListener('DOMContentLoaded', () => {
  loadHeader();
  loadSidebar();
  setTimeout(setupSidebarResizer, 300);

  // Ensure we only call onStart once per window
  if (!sessionStorage.getItem('__photosift_onstart_called')) {
    sessionStorage.setItem('__photosift_onstart_called','1');
    eel.onStart()(()=>{});
  }
});
