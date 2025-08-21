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

  // Method for posting the camera data to the backend
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
// Function to select an image file for the camera
// This will open a file dialog and set the selected file path to the input field
// It will also update the button text to indicate an image has been selected
function selectImage(selectionType = 'file'){
  eel.select_file(selectionType)((filePath) => {
    if (!filePath) return;
    document.getElementById("photo-source").value = filePath;               // store for submit
    document.getElementById("photo-of-camera-btn").textContent = "Image selected";
  });
}

// --- Common Parts Loading ---
function loadHeader() {
    fetch('commonParts/header.html')
        .then(res => res.text())
        .then(html => document.body.insertAdjacentHTML('afterbegin', html))
        .catch(err => console.error("Error loading header:", err));
}
function loadSidebar() {
    fetch('commonParts/sidebar.html')
        .then(res => res.text())
        .then(html => document.getElementById("main-container").insertAdjacentHTML('afterbegin', html))
        .catch(err => console.error("Error loading sidebar:", err));
}

window.addEventListener('DOMContentLoaded', () => {
  //loadHeader(); // Not needed here as this is in main.js
  //loadSidebar(); // Not needed here as this is in main.js
  // setTimeout(setupSidebarResizer, 300);

  // Ensure we only call onStart once per window
  if (!sessionStorage.getItem('__photosift_onstart_called')) {
    sessionStorage.setItem('__photosift_onstart_called','1');
    eel.onStart(() => {});
  }

  // Fetch and display cameras
  eel.list_cameras()((cameras) => {
    console.log("Cameras loaded:", cameras); // Should show array in browser console
    display_cameras(cameras); // NOT eel.display_cameras!
  });
});

// Function to display cameras in a table
// This function will be called with the cameras data from the backend
// It will create table rows for each camera and append them to the table body
function display_cameras(cameras) {
  const camerasTable = document.getElementById("cameras-table").getElementsByTagName('tbody')[0];
  camerasTable.innerHTML = ""; // Clear existing rows

  cameras.forEach((camera) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${camera.camera_name || ""}</td>
      <td>${camera.camera_make || ""}</td>
      <td>${camera.camera_model || ""}</td>
      <td>${camera.lens_make || ""}</td>
      <td>${camera.lens_model || ""}</td>
      <td>${camera.aperture || ""}</td>
      <td>${camera.shutter_speed || ""}</td>
      <td>${camera.iso || ""}</td>
      <td>${camera.photo_path ? `<img src="${camera.photo_path}" alt="Camera Image" width="100">` : ""}</td>
    `;
    camerasTable.appendChild(row);
  });
}
