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

async function init() {
    async function waitPyodide() {
        await new Promise(async (resolve) => {
            pyodide = await loadPyodide();
            devInfo.innerHTML += "<br>Pyodide OK!"
            fetchedNum++
            resolve()
        });
    }
    async function waitFetch(path, variable, name) {
        await new Promise(async (resolve) => {
            window[variable] = await fetchData(path);
            devInfo.innerHTML += "<br>" + name + " OK!"
            fetchedNum++
            resolve()
        });
    }
    fetchedNum = 0
    devInfo = document.getElementById("devInfo")
    devInfo.innerHTML += "OK<br><b>Fetching Four Resources</b>"
    waitPyodide()
    waitFetch("main.py", "start", "Python Script")
    waitFetch("data.json", "qadata", "JSON File")
    waitFetch("../AnalyzeR.py", "AnalyzeR", "Neural Network Script")
    async function wait() {
        delay = ms => new Promise(res => setTimeout(res, ms));
        await new Promise(async (resolve) => {

            while (fetchedNum !==4){
                await delay(100)
            }
            resolve();
        })
    }
    await wait()
    devInfo.innerHTML += "<br><b>Network Requests Complete. No More Internet Connection Required.</b><br>"
    devInfo.innerHTML += "Writing JSON Data File... "
    pyodide.FS.writeFile("/data.json", qadata)

    devInfo.innerHTML += "OK!<br>Writing Neural Network File... "
    pyodide.FS.writeFile("/home/pyodide/AnalyzeR.py", AnalyzeR)
    devInfo.innerHTML += "OK!<br>Importing Neural Network... "
    pyodide.runPython("import AnalyzeR")

    devInfo.innerHTML += "OK!<br>Running Python Script... "
    pyodide.runPython(start)
    function startBot() {
        document.getElementById("primary").innerHTML += "This is the start of your H2OBot History.<br>"
        pyodide.runPython("addQuestion()")
    }
    setTimeout(startBot, 1000)
}
async function nextQuestion(num, value) {
    pyodide.runPython('addAnswer(' + num + ',"' + value + '")')
    pyodide.runPython("addQuestion()")
}
document.addEventListener("DOMContentLoaded", function () {
    init();
});