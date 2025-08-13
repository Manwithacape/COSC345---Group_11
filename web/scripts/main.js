// FUNCTIONS HERE 
// inclutions from other js files

// Run the onStart function when the page loads

window.onload = function() {
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


