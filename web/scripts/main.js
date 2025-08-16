// FUNCTIONS HERE 
// inclutions from other js files

// Run the onStart function when the page loads

window.onload = function() {
    // Automatic loading of common elements
    loadHeader();
    loadSidebar();
    
    console.log("Page loaded, initializing Eel...");
    eel.onStart()(function() {
        console.log("Application started successfully!");
        document.getElementById("output").innerText = "Application started successfully!";
    });
};





// ------ SIDEBAR CONTROLS ------
function hideSidebar() {
    const sidebar = document.getElementById("sidebar-content");
    const resizer = document.getElementById("resizer");
    
    sidebar.style.display = "none";
    resizer.style.display = "none";
}

function showSidebar() {
    const sidebar = document.getElementById("sidebar-content");
    const resizer = document.getElementById("resizer");
    
    sidebar.style.display = "block";
    resizer.style.display = "block";
}

function toggleSidebar() {
    const sidebar = document.getElementById("sidebar-content");
    if (sidebar.style.display === "none" || sidebar.style.display === "") {
        showSidebar();
    } else {
        hideSidebar();
    }
}

// ------ COLLECTION CREATION ------

/**
 * @function handleCreateCollection
 * @description This function handles the creation of a new collection by gathering input values and calling the Eel function to create the collection.
 * @param {*} event 
 */
function handleCreateCollection(event) {
    event.preventDefault(); // Prevent form from submitting normally
    const collectionName = document.getElementById("collection-name").value;
    const collectionDescription = document.getElementById("collection-description").value;
    const collectionSource = document.getElementById("collection-source").value;
    eel.create_collection(collectionName, collectionDescription, collectionSource);
}

/**
 * Function to select a directory using Eel.
 * @function selectDirectory
 * @description This function opens a directory selection dialog and updates the input field with the selected directory
 * @param {string} selectionType - The type of selection, either 'file' or 'directory'.
 * @returns {void}
 */
function selectDirectory(selectionType = 'directory') {
    eel.select_directory(selectionType)(function(directory) {
        document.getElementById("collection-source").value = directory;
        document.getElementById("collection-source-output").innerText = "Selected Directory: " + directory;
    });
}


// ------ AUTOMATICALLY LOADED ELEMENTS ------

/**
 * @function loadHeader
 * @description This function fetches the header HTML file and inserts it into the body of the document.
 */
function loadHeader() {
    fetch('commonParts/header.html')
        .then(response => response.text())
        .then(data => {
            document.body.insertAdjacentHTML('afterbegin', data);
        })
        .catch(error => {
            console.error("Error loading header:", error);
        });
}

/**
 * @function loadSidebar
 * @description This function fetches the sidebar HTML file and inserts it into the main container of the document.
 */
function loadSidebar() {
    fetch('commonParts/sidebar.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById("main-container").insertAdjacentHTML('afterbegin', data);
        })
        .catch(error => {
            console.error("Error loading sidebar:", error);
        }); 
}
