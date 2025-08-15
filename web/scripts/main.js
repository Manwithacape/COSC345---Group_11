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

function addNumbers() {
    eel.add_numbers(1, 2)(function(result) {
        document.getElementById("output").innerText = "Result: " + result + " (from Python!)";
    });
}

function open_file() {
    eel.open_file()(function(result) {
        document.getElementById("output").innerText = "File opened: " + result;
    });
}

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

// ------ AUTOMATICALLY LOADED ELEMENTS ------
function loadHeader() {
    // open the header file and insert it into the top of the body
    fetch('commonParts/header.html')
        .then(response => response.text())
        .then(data => {
            document.body.insertAdjacentHTML('afterbegin', data);
            console.log("Header loaded successfully.");
        })
        .catch(error => {
            console.error("Error loading header:", error);
        });
}

function loadSidebar() {
    // open the sidebar file and insert it into the top of body.main
    fetch('commonParts/sidebar.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById("main-container").insertAdjacentHTML('afterbegin', data);
            console.log("Sidebar loaded successfully.");
        })
        .catch(error => {
            console.error("Error loading sidebar:", error);
        }); 
}
