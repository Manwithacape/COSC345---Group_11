// FUNCTIONS HERE 
// inclutions from other js files
include('eel.js');
include('math.js');

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