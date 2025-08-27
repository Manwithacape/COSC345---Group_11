
// --- Collection Card Logic ---
/**
 * @function createCollectionCard
 * @description Creates a collection card element with a thumbnail image, title, and date.
 * @param {String} name 
 * @param {String} imagePath 
 * @param {String} dateTime 
 * @returns {HTMLElement} card
 */
function createCollectionCard(name="NO NAME", imagePath, dateTime="00-00 00:00:00") {
    const card = document.createElement("a");
    card.className = "collection-card";
    card.href = "collection-view.html";

    const img = document.createElement("img");
    img.className = "collection-card-image";
    img.src = imagePath;
    img.alt = `Collection Thumbnail for ${name}`;

    const header = document.createElement("div");
    header.className = "collection-card-header";

    const title = document.createElement("h2");
    title.className = "underline";
    title.textContent = name;

    const date = document.createElement("h4");
    date.textContent = dateTime;

    header.append(title, date);
    card.append(img, header);

    const tag = document.createElement("div");
    tag.className = "collection-card-tag";

    card.appendChild(tag);
    return card;
}

/**
 * @function addCollectionCardToGrid
 * @description Adds a collection card to a specified grid element.
 * @param {HTMLElement} card 
 * @param {HTMLElement} gridId 
 */
function addCollectionCardToGrid(card, gridId = "collection-card-grid") {
    const grid = document.getElementById(gridId);
    if (grid) {
        grid.appendChild(card);
    } else {
        console.error(`Grid with ID '${gridId}' not found.`);
    }
}

/**
 * @function loadCollectionCardsSequentially
 * @description Loads collection cards sequentially from an array of collections recusively.
 * @param {Array} collections 
 * @param {Int} index - The current index in the collections array. 
 * @returns nothing
 */
function loadCollectionCardsSequentially(collections, index = 0) {
    if (index >= collections.length) return;
    const col = collections[index];
    const imgPath = col.thumbnail_path || null; // FIXED: use thumbnail_path
    const card = createCollectionCard(col.name, "images/Icons/General Icons/photo.png", col.date_created); // FIXED: use date_created
    if (imgPath) {
        eel.get_image_data_url(imgPath)(function(dataUrl) {
            if (dataUrl) {
                card.querySelector('.collection-card-image').src = dataUrl;
            }
            addCollectionCardToGrid(card);
            loadCollectionCardsSequentially(collections, index + 1);
        });
    } else {
        addCollectionCardToGrid(card);
        loadCollectionCardsSequentially(collections, index + 1);
    }
}

// ------ SIDEBAR LOGIC ------
/**
 * @function hideSidebar
 * @description Hides the sidebar and updates the toggle button icon.
 */
function hideSidebar() {
    setSidebarDisplay("none", "show-hollow.png", "show sidebar icon", false);
}

/**
 * @function showSidebar
 * @description Shows the sidebar and updates the toggle button icon.
 */
function showSidebar() {
    setSidebarDisplay("flex", "hide-hollow.png", "hide sidebar icon", true);
    // reset sidebar width when showing
    const sidebarContent = document.getElementById("sidebar-content");
    sidebarContent.style.width = "250px"; // Reset width when showing
}

/**
 * @function toggleSidebar
 * @description Toggles the sidebar visibility and updates the toggle button icon.
 */
function toggleSidebar() {
    const sidebar = document.getElementById("sidebar-content");
    if (sidebar.style.display === "none" || sidebar.style.display === "") {
        showSidebar();
    } else {
        hideSidebar();
    }
}

/**
 * @function setSidebarDisplay
 * @description Sets the display properties of the sidebar and updates the toggle button icon.
 * @param {String} display 
 * @param {String} icon 
 * @param {String} alt 
 * @param {String} border 
 */
function setSidebarDisplay(display, icon, alt, border=true) {
    const sidebar = document.getElementById("sidebar");
    const sidebarContent = document.getElementById("sidebar-content");
    const resizer = document.getElementById("resizer");
    const toggleButton = document.getElementById("toggle-sidebar");
    sidebarContent.style.display = display;
    resizer.style.display = display;
    if (border) {
        sidebar.style.borderRight = "1px solid var(--border-color)";
    } else {
        sidebar.style.borderRight = "none";
    }
    toggleButton.src = `images/icons/Sidebar Controls/${icon}`;
    toggleButton.alt = alt;
}

// --- Sidebar Resizer Logic ---

/**
 * @function setupSidebarResizer
 * @description Initializes the sidebar resizer functionality.
 */
function setupSidebarResizer() {
    const resizer = document.getElementById("resizer");
    const sidebarContent = document.getElementById("sidebar-content");
    const sidebarControls = document.getElementById("sidebar-controls");
    let isResizing = false;

    resizer.addEventListener("mousedown", function(e) {
        isResizing = true;
        document.body.style.cursor = "ew-resize";
    });

    document.addEventListener("mousemove", function(e) {
        if (!isResizing) return;
        const newWidth = e.clientX - sidebarContent.getBoundingClientRect().left;
        const maxWidth = 800; // Set your desired max width in px
        sidebarContent.style.width = `${Math.max(0, Math.min(newWidth, maxWidth))}px`; // Clamp between 0 and maxWidth

        // if the sidebar is less than or equal to 5px, hide it
        const widthValue = parseInt(sidebarContent.style.width, 10);
        const controlsWidth = parseInt(getComputedStyle(sidebarControls).width, 10);
        if (widthValue <= controlsWidth) {
            hideSidebar();
        }
    });

    document.addEventListener("mouseup", function() {
        if (isResizing) {
            isResizing = false;
            document.body.style.cursor = "";
        }
    });
}
// --- Collection Creation Logic ---

/**
 * @function handleCreateCollection
 * @description Handles the creation of a new collection by gathering input values and calling the eel function to create the collection.
 * @param {Event} event 
 */
function handleCreateCollection(event) {
    event.preventDefault();
    const name = document.getElementById("collection-name").value;
    const desc = document.getElementById("collection-description").value;
    const source = document.getElementById("collection-source").value;
    eel.create_collection(name, desc, source);
    window.location.href = "dashboard.html";
}

/**
 * @function selectDirectory
 * @description Opens a directory selection dialog and sets the selected directory path to the input field.
 * @param {String} selectionType - The type of selection, default is 'directory'.
 */
function selectDirectory(selectionType = 'directory') {
    eel.select_directory(selectionType)(function(directory) {
        document.getElementById("collection-source").value = directory;
        document.getElementById("collection-source-output").innerText = `Selected Directory: ${directory}`;
    });
}

// --- Common Parts Loading ---
/**
 * @function loadHeader
 * @description Loads the header HTML into the document body.
 */
function loadHeader() {
    fetch('commonParts/header.html')
        .then(res => res.text())
        .then(html => document.body.insertAdjacentHTML('afterbegin', html))
        .catch(err => console.error("Error loading header:", err));
}

/**
 * @function loadSidebar
 * @description Loads the sidebar HTML into the main container.
 */
function loadSidebar() {
    fetch('commonParts/sidebar.html')
        .then(res => res.text())
        .then(html => document.getElementById("main-container").insertAdjacentHTML('afterbegin', html))
        .catch(err => console.error("Error loading sidebar:", err));
}

// --- Event Listener Setup ---
window.addEventListener('DOMContentLoaded', () => {
    loadHeader();
    loadSidebar();

    // Setup sidebar resizer after sidebar loads
    setTimeout(setupSidebarResizer, 300); // Delay to ensure sidebar is loaded

    // Restore selectDirectory button functionality
    const selectDirBtn = document.getElementById("select-directory-btn");
    if (selectDirBtn) {
        selectDirBtn.addEventListener("click", () => {
            selectDirectory();
        });
    }

    // Restore sidebar toggle functionality
    const toggleSidebarBtn = document.getElementById("toggle-sidebar");
    if (toggleSidebarBtn) {
        toggleSidebarBtn.addEventListener("click", () => {
            toggleSidebar();
        });
    }

    eel.get_all_collections()(collections => {
        if (Array.isArray(collections)) {
            loadCollectionCardsSequentially(collections);
        }
    });

    eel.onStart()(() => {
        const output = document.getElementById("output");
        if (output) output.innerText = "Application started successfully!";
    });

    const findDupBtn = document.getElementById("find-duplicates-btn");
    if (findDupBtn) {
        findDupBtn.addEventListener("click", () => {

            eel.get_all_collections()((collections) => {
                let imagePaths = [];
                collections.forEach(col => {
                    if (Array.isArray(col.photos)){
                        col.photos.forEach(photo => {
                            imagePaths.push(photo)
                        });
                    }
                });
                
                console.log("Sending to Python: ", imagePaths);
        
                eel.detect_duplicates(imagePaths, 0.99, 10)(function(result) {
                    console.log("Duplicates:", result.duplicates);
                    console.log("Near duplicates:", result.near_duplicates);
        
                    const outputDiv = document.getElementById("duplicate-results");
                    outputDiv.innerHTML = "";
        
                    if (result.duplicates.length === 0 && result.near_duplicates.length === 0) {
                        outputDiv.innerText = "No duplicates found!";
                    } else {
                        result.duplicates.forEach(d => {
                            outputDiv.innerHTML += `<p>Duplicate (score ${d[0].toFixed(3)}): ${d[1]} & ${d[2]}</p>`;
                        });
                        result.near_duplicates.forEach(d => {
                            outputDiv.innerHTML += `<p>Near Duplicate (score ${d[0].toFixed(3)}): ${d[1]} & ${d[2]}</p>`;
                        });
                    }
                });
            });
            
        });
    }
});
