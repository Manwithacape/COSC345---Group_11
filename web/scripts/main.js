// FUNCTIONS HERE 
// inclutions from other js files

// Run the onStart function when the page loads

window.onload = function() {
    // Automatic loading of common elements
    loadHeader();
    loadSidebar();

    // Debug collection card creation
    createCollectionCard("Example Collection 1", "images/doomtda.jpeg", "03/07/2003");
    createCollectionCard("Example Collection 2", "images/doomtda.jpeg", "04/07/2003");
    createCollectionCard("Example Collection 3", "images/doomtda.jpeg", "05/07/2003");
    addCollectionCardToGrid(createCollectionCard("Example Collection 1", "images/doomtda.jpeg", "03/07/2003"));
    addCollectionCardToGrid(createCollectionCard("Example Collection 2", "images/doomtda.jpeg", "04/07/2003"));
    addCollectionCardToGrid(createCollectionCard("Example Collection 3", "images/doomtda.jpeg", "05/07/2003"));

    
    console.log("Page loaded, initializing Eel...");
    eel.onStart()(function() {
        console.log("Application started successfully!");
        document.getElementById("output").innerText = "Application started successfully!";
    });
};

/**
 * @function createCollectionCard
 * @description This function creates a collection card element that displays the collection's name, image, and date/time.
 * @param {string} collection_name - Display name and identifier for the collection.
 * @param {string} colletion_image_path - Path to the collection's thumbnail image.
 * @param {string} collection_date_time - Date and time associated with the collection, formatted as a string.
 * @returns {Element} - Returns a collection card element.
 * @example
 *  <a class="collection-card" href="collection-view.html">
        <img class="collection-card-image" src="collection_image_path" alt="Collection Thumbnail for {collection_name}">
        <div class="collection-card-header">
            <h2 class="underline">{collection_name}</h2>
            <h4>{collection_date_time}</h4>
        </div>
        <div class="collection-card-tag"></div>
    </a>
 */
function createCollectionCard(collection_name, colletion_image_path, collection_date_time) {
    /*
    <a class="collection-card" href="collection-view.html">
        <img class="collection-card-image" src="collection_image_path" alt="Collection Thumbnail for {collection_name}">
        <div class="collection-card-header">
            <h2 class="underline">{collection_name}</h2>
            <h4>{collection_date_time}</h4>
        </div>
        <div class="collection-card-tag"></div>
    </a>
    */

    const collectionCard = document.createElement("a");
    collectionCard.className = "collection-card";
    collectionCard.href = "collection-view.html"; // Link to the collection view page

    const collectionImage = document.createElement("img");
    collectionImage.className = "collection-card-image";
    collectionImage.src = colletion_image_path; // Set the image source
    collectionImage.alt = "Collection Thumbnail for " + collection_name; // Alt text for accessibility

    const collectionHeader = document.createElement("div");
    collectionHeader.className = "collection-card-header";
    const collectionTitle = document.createElement("h2");
    collectionTitle.className = "underline";
    collectionTitle.textContent = collection_name; // Set the collection name

    const collectionDate = document.createElement("h4");
    collectionDate.textContent = collection_date_time; // Set the collection date

    const collectionTag = document.createElement("div");
    collectionTag.className = "collection-card-tag"; // This can be used for tags or

    collectionHeader.appendChild(collectionTitle);
    collectionHeader.appendChild(collectionDate);
    collectionCard.appendChild(collectionImage);
    collectionCard.appendChild(collectionHeader);
    collectionCard.appendChild(collectionTag);

    return collectionCard; // Return the complete collection card element
}

/**
 * @function addCollectionCardToGrid
 * @description This function adds a collection card to the specified grid element in the dashboard.html.
 * @param {Element} collectionCard 
 * @param {String} gridId 
 */
function addCollectionCardToGrid(collectionCard, gridId = "collection-card-grid") {
    const grid = document.getElementById(gridId);
    if (grid) {
        grid.appendChild(collectionCard); // Append the collection card to the grid
    } else {
        console.error("Grid with ID '" + gridId + "' not found.");
    }
}

// ------ SIDEBAR CONTROLS ------
function hideSidebar() {
    const sidebar = document.getElementById("sidebar-content");
    const resizer = document.getElementById("resizer");
    const toggleButton = document.getElementById("toggle-sidebar");

    sidebar.style.display = "none";
    resizer.style.display = "none";
    toggleButton.src = "images/icons/Sidebar Controls/show-hollow.png"; // Change icon to show sidebar
    toggleButton.alt = "show sidebar icon"; // Update alt text for accessibility
}

function showSidebar() {
    const sidebar = document.getElementById("sidebar-content");
    const resizer = document.getElementById("resizer");
    const toggleButton = document.getElementById("toggle-sidebar");
    
    sidebar.style.display = "block";
    resizer.style.display = "block";
    toggleButton.src = "images/icons/Sidebar Controls/hide-hollow.png"; // Change icon to hide sidebar
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
