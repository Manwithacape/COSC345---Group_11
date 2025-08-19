
// --- Collection Card Logic ---
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



function addCollectionCardToGrid(card, gridId = "collection-card-grid") {
    const grid = document.getElementById(gridId);
    if (grid) {
        grid.appendChild(card);
    } else {
        console.error(`Grid with ID '${gridId}' not found.`);
    }
}

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
            loadCollectionCardsSequentially(collections, index + 1);
        });
    } else {
        addCollectionCardToGrid(card);
        loadCollectionCardsSequentially(collections, index + 1);
    }
}

// --- Sidebar Logic ---
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
        sidebar.style.width = "250px"; // Reset width when showing
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

// --- Sidebar Resizer Logic ---
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
function handleCreateCollection(event) {
    event.preventDefault();
    const name = document.getElementById("collection-name").value;
    const desc = document.getElementById("collection-description").value;
    const source = document.getElementById("collection-source").value;
    eel.create_collection(name, desc, source);
    window.location.href = "dashboard.html";
}
function selectDirectory(selectionType = 'directory') {
    eel.select_directory(selectionType)(function(directory) {
        document.getElementById("collection-source").value = directory;
        document.getElementById("collection-source-output").innerText = `Selected Directory: ${directory}`;
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
});
