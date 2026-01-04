async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const fetchdata = await response.text();
        return fetchdata;
    } catch (error) {
        console.error('Error fetching data:', error);
        return;
    }
}

// Add delay to code in ms
delay = ms => new Promise(res => setTimeout(res, ms));

function appendPrimary(text, pos) {
    if (pos == 0) {
        primary.insertAdjacentHTML(
            "beforeend", "<div class='leftMessage'>" + text + "</div>"
        )
    } else if (pos == 1) {
        primary.insertAdjacentHTML(
            "beforeend", "<div class='rightMessage'>" + text + "</div>"
        )
    } else {
        primary.insertAdjacentHTML("beforeend", text)
    }
    primary.scrollTop = primary.scrollHeight
}

function addQuestion() {
    if (questionID == "END") {
        appendPrimary("This is the end of your H2OBot History.<br><br>", -1)
    } else {
        appendPrimary(data[questionID]["q"], 0)
    }
}

function addOptions() {
    function formatAns(text) {
        i++
        return (
            '<button class="button" onclick="nextQuestion(this.value,this.innerText)" value="'
            + String(i)
            + '">'
            + String(text["o"])
            + "</button>"
        )
    }
    if (questionID != "END") {
        i = -1
        secondary.innerHTML = data[questionID]["a"].map(x => formatAns(x)).join("")
    }
}

function addResponse(answer) {
    appendPrimary(answer, 1)
    secondary.innerHTML = ""
}

function addAnswer(num) {
    ans = data[questionID]["a"][num]
    appendPrimary(ans["r"], 0)
    questionID = ans["n"]
}

// Initiate on page load
async function init() {
    useNN = false
    questionID = "START"
    // Wait for pyodide to load
    async function waitPyodide() {
        await new Promise(async (resolve) => {
            fetchedNum--
            pyodide = await loadPyodide();
            devInfo.innerHTML += "<br>Pyodide OK!"
            fetchedNum++
            resolve()
        });
    }
    // Wait for fetched resource
    async function waitFetch(path, variable, name) {
        await new Promise(async (resolve) => {
            fetchedNum--
            window[variable] = await fetchData(path);
            devInfo.innerHTML += "<br>" + name + " OK!"
            fetchedNum++
            resolve()
        });
    }
    fetchedNum = 0
    devInfo = document.getElementById("devInfo")
    devInfo.innerHTML += "OK<br><b>Fetching Resources</b>"
    if (useNN) {
        waitPyodide()
        waitFetch("main.py", "start", "Python Script")
    }
    waitFetch("data.json", "qadata", "JSON File")
    if (useNN) { waitFetch("../AnalyzeR.py", "AnalyzeR", "Neural Network Script") }
    await delay(500)
    // Wait for all resources to fetch
    async function wait() {
        await new Promise(async (resolve) => {

            while (fetchedNum !== 0) {
                await delay(100)
            }
            resolve();
        })
    }
    await wait()
    await delay(100)
    data = JSON.parse(qadata)
    devInfo.innerHTML += "<br><b>Network Requests Complete. No More Internet Connection Required.</b><br>"

    if (useNN) {
        devInfo.innerHTML += "Writing JSON Data File... "
        pyodide.FS.writeFile("/data.json", qadata)
        devInfo.innerHTML += "<br>Writing Neural Network File... "
        pyodide.FS.writeFile("/home/pyodide/AnalyzeR.py", AnalyzeR)
        devInfo.innerHTML += "<br>Running Python Script... "
        pyodide.runPython(start)
    }
    devInfo.innerHTML += (`
        <br><b>Starting H2OBot...</b><br><br>
        <button class="link cn"onclick="document.getElementById('devInfo').innerHTML = ''">
        <b>Hide Initiation Log</b></button><hr><br>
    `)
    await delay(500)
    document.getElementById("primary").innerHTML += "This is the start of your H2OBot History.<br>"
    await delay(500)
    addQuestion()
    await delay(500)
    addOptions()
}

// Run by button press, to add answer to question and then 
async function nextQuestion(num, value) {
    addResponse(value)
    await delay(500)
    addAnswer(num)
    await delay(500)
    addQuestion()
    await delay(500)
    addOptions()
}


document.addEventListener("DOMContentLoaded", function () {
    init();
});