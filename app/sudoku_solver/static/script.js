'use strict';


//==================================================================================================
// Prepare Variables
//==================================================================================================
let table = [[], [], [], [], [], [], [], [], []];
let requestId = 0;
let selectedCell = "00";

const tableEl = document.querySelector(".table");
const btnBack = document.querySelector(".back");
const btnSolve = document.querySelector(".solve");
const btnClear = document.querySelector(".clear");

const notifyText = document.querySelector(".notify-text");

const loader = document.querySelector(".loader");
const loaderText = document.querySelector(".loader-text");


//==================================================================================================
// Functions
//==================================================================================================
//--------------------------
// Private Functions
//--------------------------
const getValues = function() {
    for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 9; j++) {
            table[i].push(Number(document.getElementById(`${i}${j}`).value));
        }
    }
};

const setValues = function(table) {
    for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 9; j++) {
            document.getElementById(`${i}${j}`).value = Number(table[i][j]);
        }
    }
};

const resetValues = function() {
    for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 9; j++) {
            document.getElementById(`${i}${j}`).value = "";
        }
    }
};

const disableInput = function(disable) {
    for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 9; j++) {
            if (disable) {
                document.getElementById(`${i}${j}`).setAttribute("disabled", true);
            }
            else {
                document.getElementById(`${i}${j}`).removeAttribute("disabled");
            }
        }
    }
};

const postTable = async function(reqId) {
    // Prepare message
    const req = {
        table: table,
        reqId: reqId,
        msg: ""
    };

    // Create Promise
    const promise = await fetch("/sudoku-solver/table", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(req)
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error: ${response.status}`);
            }
        })
        .catch((err) => console.error(err));

    // Reset table
    table = [[], [], [], [], [], [], [], [], []];

    // Return Promise
    return promise;
};

const getTableCalc = async function(reqId) {
    // Create Promise
    const promise = await fetch(`/sudoku-solver/table/${reqId}`, { method: "GET"})
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            if (Number(data.reqId) !== Number(requestId)) {     // MF: Ignore if not expected reqId
                return;
            }
            if (!data.table) {
                // Set and display Notify Text
                notifyText.textContent = data.msg;
                notifyText.classList.remove("hidden");
                return;
            }
            if (Number(data.reqId) === Number(requestId)) {
                setValues(data.table);
                disableInput(true);
                btnSolve.setAttribute("disabled", true);
            }
        })
        .catch(err => console.error(err));

    // Return Promise
    return promise;
};

//--------------------------
// Public Functions
//--------------------------
const solve = async function() {
    // Prepare Id
    const reqId = requestId;

    // Set Notify Text and Loader
    notifyText.classList.add("hidden");
    loader.classList.remove("hidden");
    loaderText.classList.remove("hidden");

    // Get Values from cells
    getValues();

    // Post Data to Server
    await postTable(reqId);

    // Get Data from Server
    await getTableCalc(reqId);

    // Hide Loader
    if (reqId === requestId) {      // MF: Ignore if not expected reqId
        loader.classList.add("hidden");
        loaderText.classList.add("hidden");
    }
}

const clear = async function() {
    // Increment request counter
    requestId++;

    // Clear all cells in Table and enable input
    resetValues()
    disableInput(false)
    btnSolve.removeAttribute("disabled");

    // Hide Notify Text and Loader
    notifyText.classList.add("hidden");
    loader.classList.add("hidden");
    loaderText.classList.add("hidden");
}


//==================================================================================================
// Event handlers
//==================================================================================================
btnBack.addEventListener("click", () => window.location.href = "/");

btnSolve.addEventListener("click", solve);

btnClear.addEventListener("click", clear);

tableEl.addEventListener("click", (event) => {
    if (event.target.id !== "") {       // MF: Check if user click on a cell, not somewhere else on table
        selectedCell = event.target.id
    }
});

document.addEventListener('keydown', (event) => {
    // Navigate back if escape pressed
    if (event.key === "Escape") {
        event.preventDefault();         // MF: To prevent cancelation of loading the page when "Escape" is pressed
        window.location.href = "/";
    }

    // Solve if enter pressed
    if (event.key === "Enter") {
        solve();
    }

    // Clear if delete pressed
    if (event.key === "Delete") {
        clear();
    }

    // Arrow keys
    if (event.key === "ArrowLeft") {
        if (Number(selectedCell[1]) > 0) {
            selectedCell = selectedCell[0] + (Number(selectedCell[1]) - 1)
        }
    }
    if (event.key === "ArrowUp") {
        if (Number(selectedCell[0]) > 0) {
            selectedCell = (Number(selectedCell[0]) - 1) + selectedCell[1]
        }
    }
    if (event.key === "ArrowRight") {
        if (Number(selectedCell[1]) < 8) {
            selectedCell = selectedCell[0] + (Number(selectedCell[1]) + 1)
        }
    }
    if (event.key === "ArrowDown") {
        if (Number(selectedCell[0]) < 8) {
            selectedCell = (Number(selectedCell[0]) + 1) + selectedCell[1]
        }
    }
    document.getElementById(selectedCell).focus();
});

function inNumOnly(input) {     // MF: Handles that user can type only num 1-9
    input.value = input.value.replace(/[^1-9]/g, '');
}


//==================================================================================================
// Init
//==================================================================================================
document.getElementById(selectedCell).focus();
