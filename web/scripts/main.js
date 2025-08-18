// --- Automatic Element Loading ---

function loadCollectionCardsSequentially(collections, index = 0) {
    if (index >= collections.length) return;

    const col = collections[index];
    const imgPath = col.preview || null;
    const card = createCollectionCard(col.name, "images/Icons/General Icons/photo.png", col.created_on);

    if (imgPath) {
        eel.get_image_data_url(imgPath)(function(dataUrl) {
            if (dataUrl) {
                card.querySelector('.collection-card-image').src = dataUrl;
            }
            addCollectionCardToGrid(card);
            // Load the next card after this one finishes
            loadCollectionCardsSequentially(collections, index + 1);
        });
    } else {
        addCollectionCardToGrid(card);
        loadCollectionCardsSequentially(collections, index + 1);
    }
}

window.onload = function() {
    loadHeader();
    loadSidebar();

    eel.get_all_collections()(function(collections) {
        if (Array.isArray(collections)) {
            loadCollectionCardsSequentially(collections);
        }
    });

    console.log("Page loaded, initializing Eel...");
    eel.onStart()(function() {
        console.log("Application started successfully!");
        const output = document.getElementById("output");
        if (output) output.innerText = "Application started successfully!";
    });
};

// --- Collection Card Functions ---
/**
 * Creates a collection card element.
 * @param {string} name - Collection name.
 * @param {string} imagePath - Thumbnail image path.
 * @param {string} dateTime - Collection date/time.
 * @returns {Element}
 */
function createCollectionCard(name, imagePath, dateTime) {
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
 * Adds a collection card to the grid.
 * @param {Element} card
 * @param {string} gridId
 */
function addCollectionCardToGrid(card, gridId = "collection-card-grid") {
    const grid = document.getElementById(gridId);
    if (grid) {
        grid.appendChild(card);
    } else {
        console.error(`Grid with ID '${gridId}' not found.`);
    }
}

// --- Sidebar Controls ---
function hideSidebar() {
    setSidebarDisplay("none", "show-hollow.png", "show sidebar icon", false);
}

function showSidebar() {
    setSidebarDisplay("block", "hide-hollow.png", "hide sidebar icon", true);
}

function toggleSidebar() {
    const sidebar = document.getElementById("sidebar-content");
    if (sidebar.style.display === "none" || sidebar.style.display === "") {
        showSidebar();
    } else {
        hideSidebar();
    }
}

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

// --- Collection Creation ---
function handleCreateCollection(event) {
    event.preventDefault();
    const name = document.getElementById("collection-name").value;
    const desc = document.getElementById("collection-description").value;
    const source = document.getElementById("collection-source").value;
    eel.create_collection(name, desc, source);

    // redirect to dashboard after creation
    window.location.href = "dashboard.html";
}

/**
 * Opens a directory selection dialog and updates the input field.
 * @param {string} selectionType
 */
function selectDirectory(selectionType = 'directory') {
    eel.select_directory(selectionType)(function(directory) {
        document.getElementById("collection-source").value = directory;
        document.getElementById("collection-source-output").innerText = `Selected Directory: ${directory}`;
    });
}

// --- Load Common Parts ---
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
