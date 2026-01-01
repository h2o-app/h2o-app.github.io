async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.text();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
        return;
    }
}
var pyodide
var next
async function init() {
    document.getElementById("primary").innerHTML += "OK<br>Loading Pyodide... "
    pyodide = await loadPyodide();
    document.getElementById("primary").innerHTML += "OK<br>"
    document.getElementById("primary").innerHTML += "Fetching Python Script... "
    let start = await fetchData("main.py")
    document.getElementById("primary").innerHTML += "OK<br>"
    document.getElementById("primary").innerHTML += "Fetching JSON Data... "
    let qadata = await fetchData("data.json")
    document.getElementById("primary").innerHTML += "OK<br>"
    document.getElementById("primary").innerHTML += "Fetching Neural Network Script File... "
    let AnalyzeR = await fetchData("../AnalyzeR.py")
    document.getElementById("primary").innerHTML += "OK<br><b>Network Requests Complete. No More Internet Connection Required.</b><br>"
    document.getElementById("primary").innerHTML += "Writing JSON Data File... "
    pyodide.FS.writeFile("/data.json", qadata)
    document.getElementById("primary").innerHTML += "OK<br>"
    document.getElementById("primary").innerHTML += "Writing Neural Network File... "
    pyodide.FS.writeFile("/home/pyodide/AnalyzeR.py", AnalyzeR)
    document.getElementById("primary").innerHTML += "OK<br>"
    document.getElementById("primary").innerHTML += "Importing Neural Network... "
    pyodide.runPython("import AnalyzeR")
    document.getElementById("primary").innerHTML += "OK<br>"
    document.getElementById("primary").innerHTML += "Running Python Script... "
    pyodide.runPython(start)
    function startBot() {
        primary.innerHTML = ""
        pyodide.runPython("addQuestion()")
    }
    setTimeout(startBot, 5000)
}
async function nextQuestion(num, value) {
    pyodide.runPython('addAnswer(' + num + ',"' + value + '")')
    pyodide.runPython("addQuestion()")
}
init();